"""数据接入：扫 data/raw/，识别文件类型与节点 ID，去重合并到 interim parquet。

支持两种目录结构：
  旧式（flow/level 分离）:  raw/nodes_flow/<node>.csv  raw/nodes_level/<node>.csv
  新式（按管网类型分目录）:  raw/nodes/污水/<location>.xlsx  raw/nodes/雨水/<location>.xlsx

新式 Excel 格式规范（平台导出）:
  - 第 0 行: 合并单元格，内容为"位置名-液位计"
  - 第 1 行: 列名 → 累计流量(m³) / 流量(m³/s) / 流速(m/s) / 水温(℃) / 液位(m) / 创建时间 / 读取时间
  - 第 2 行起: 数据（读取时间 = 10min 对齐的规范时刻）

节点 ID 匹配优先级（新式格式）:
  1. 文件名中包含规范 ID 正则（旧式兼容）
  2. 文件名 stem 或 Excel 首行列名 匹配 sites.yaml 的 road / pinyin 字段
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import pandas as pd

from .io_paths import paths, settings, sites as load_sites


# ---------------------------------------------------------------------------
# 文件扫描
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RawFile:
    path: Path
    kind: str   # plant_inlet | nodes_flow | nodes_level | rainfall
                # nodes_sewage | nodes_stormwater  (新式目录)
    sha256: str
    mtime: float


def scan_raw() -> list[RawFile]:
    """扫描 data/raw/ 下所有支持扩展名的文件。"""
    p = paths()
    accept = set(settings().get("ingest", {}).get("accept_extensions", [".csv", ".xlsx", ".xls", ".txt"]))
    items: list[RawFile] = []

    # 旧式目录
    for kind, root in [
        ("plant_inlet",  p.raw_plant),
        ("nodes_flow",   p.raw_nodes_flow),
        ("nodes_level",  p.raw_nodes_level),
        ("rainfall",     p.raw_rainfall),
    ]:
        if not root.exists():
            continue
        for f in root.rglob("*"):
            if f.is_file() and f.suffix.lower() in accept and not f.name.startswith("."):
                items.append(RawFile(path=f, kind=kind,
                                     sha256=_hash_file(f), mtime=f.stat().st_mtime))

    # 新式目录：raw/nodes/污水/ 和 raw/nodes/雨水/
    nodes_root = p.raw / "nodes"
    if nodes_root.exists():
        for subdir, kind in [("污水", "nodes_sewage"), ("雨水", "nodes_stormwater")]:
            d = nodes_root / subdir
            if not d.exists():
                continue
            for f in d.rglob("*"):
                if f.is_file() and f.suffix.lower() in accept and not f.name.startswith("."):
                    items.append(RawFile(path=f, kind=kind,
                                         sha256=_hash_file(f), mtime=f.stat().st_mtime))

    return items


def _hash_file(p: Path, *, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# 通用读取器（旧式格式）
# ---------------------------------------------------------------------------

def _read_any(p: Path) -> pd.DataFrame:
    if p.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(p)
    for enc in ["utf-8", "utf-8-sig", "gbk", "gb18030"]:
        try:
            return pd.read_csv(p, encoding=enc)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(p, encoding="latin-1", on_bad_lines="skip")


def _find_ts_column(df: pd.DataFrame) -> str | None:
    """按优先级列表在 df 列名中匹配时间戳列。"""
    candidates = settings().get("ingest", {}).get("ts_column_candidates",
                    ["timestamp", "time", "ts", "datetime", "采集时间", "时间", "数据时间"])
    cols_lower = {c.lower(): c for c in df.columns.astype(str)}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    for col in df.columns:
        cl = str(col).lower()
        if "time" in cl or "时间" in str(col):
            return col
    return None


# ---------------------------------------------------------------------------
# 节点 ID 提取
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _location_index() -> dict[str, str]:
    """构建 {位置名/拼音 → node_id} 反向索引，来自 sites.yaml。"""
    cfg = load_sites()
    idx: dict[str, str] = {}
    for nid, info in (cfg.get("nodes") or {}).items():
        for key in ("road", "pinyin"):
            val = (info.get(key) or "").strip()
            if val:
                idx[val] = nid
                # 去掉括号、空格的归一化版本，提升容错
                norm = re.sub(r"[\s（）()【】]", "", val)
                idx[norm] = nid
    return idx


def _norm_location(s: str) -> str:
    return re.sub(r"[\s（）()【】]", "", s)


def _extract_node_id(path: Path, df: pd.DataFrame) -> str | None:
    """从文件名或表列中提取规范 node_id。

    匹配顺序：
    1. 文件名中的规范 ID 正则（S01-S10 / W11-W19...）
    2. sites.yaml location_index 按文件名 stem 查找
    3. sites.yaml location_index 按 Excel 首行列名查找
    4. 表内 node_id / 节点编号 等列的正则匹配
    """
    pat = settings().get("ingest", {}).get("node_id_pattern", r"(S\d{2}|W\d{2})")

    # 1. 文件名正则
    m = re.search(pat, path.name)
    if m:
        return m.group(1)

    # 2. 文件名 stem → location_index
    stem = path.stem
    # 去掉"-监测数据-YYYYMMDDHHMMSS"后缀
    clean_stem = re.sub(r"-监测数据-\d{12,}$", "", stem)
    clean_stem = re.sub(r"-监测数据$", "", clean_stem).strip()
    idx = _location_index()
    if clean_stem in idx:
        return idx[clean_stem]
    if _norm_location(clean_stem) in idx:
        return idx[_norm_location(clean_stem)]

    # 3. Excel 首行列名（新式格式：第 0 列 = "位置名-液位计"）
    if not df.empty:
        first_col = str(df.columns[0])
        # 去掉 "-液位计" 等后缀
        loc_from_col = re.sub(r"-液位计.*$", "", first_col).strip()
        if loc_from_col in idx:
            return idx[loc_from_col]
        if _norm_location(loc_from_col) in idx:
            return idx[_norm_location(loc_from_col)]

    # 4. 表内列
    for c in ("node_id", "节点", "节点编号", "site_id"):
        if c in df.columns:
            for v in df[c].dropna().astype(str).head(20):
                m = re.search(pat, v)
                if m:
                    return m.group(1)

    return None


def _extract_station_id(path: Path, df: pd.DataFrame) -> str | None:
    m = re.search(r"(V\d{4,5})", path.name)
    if m:
        return m.group(1)
    for c in ("station_id", "雨量站", "station", "区站号(字符)", "区站号"):
        if c in df.columns:
            for v in df[c].dropna().astype(str).head(20):
                m = re.search(r"(V\d{4,5})", v)
                if m:
                    return m.group(1)
    return None


# ---------------------------------------------------------------------------
# 字段别名映射
# ---------------------------------------------------------------------------

PLANT_FIELD_ALIASES = {
    "flow_m3s": ["flow", "流量", "进水流量", "瞬时流量", "Q"],
    "ph":        ["pH", "ph", "酸碱度"],
    "cod_mgL":   ["COD", "cod", "化学需氧量"],
    "nh3n_mgL":  ["NH3-N", "氨氮", "ammonia", "NH3N"],
    "temp_c":    ["temp", "水温", "temperature"],
}

LEVEL_FIELD_ALIASES  = ["level_m", "level", "液位", "水位", "depth", "液位(m)"]
FLOW_FIELD_ALIASES   = ["flow_m3s", "flow", "流量", "Q", "流量(m³/s)"]
VELOCITY_FIELD_ALIASES = ["velocity_ms", "velocity", "流速", "v", "流速(m/s)"]
RAIN_FIELD_ALIASES   = ["rain_mm_h", "rain", "降雨", "降水", "rainfall", "rain_mm",
                         "过去1小时降水量"]


def _pick_first(df: pd.DataFrame, candidates: list[str]) -> pd.Series | None:
    """在 df 中按候选列名列表返回第一个匹配的数值列。"""
    for c in candidates:
        if c in df.columns:
            return pd.to_numeric(df[c], errors="coerce")
        for col in df.columns:
            if str(col).lower() == c.lower() or c.lower() in str(col).lower():
                return pd.to_numeric(df[col], errors="coerce")
    return None


def _pick_flow_with_unit(df: pd.DataFrame) -> pd.Series | None:
    """检测流量单位，若为 m³/h 则自动除以 3600 转为 m³/s。"""
    for c in FLOW_FIELD_ALIASES:
        for col in df.columns:
            col_str = str(col)
            if c.lower() in col_str.lower() or col_str.lower() == c.lower():
                series = pd.to_numeric(df[col], errors="coerce")
                if "m³/h" in col_str or "m3/h" in col_str.lower():
                    series = series / 3600.0
                return series
    return None


# ---------------------------------------------------------------------------
# 新式节点 Excel（header=1）
# ---------------------------------------------------------------------------

def _read_node_excel(path: Path) -> tuple[str, pd.DataFrame]:
    """读取平台导出的 2 行表头 Excel。

    Returns:
        (location_name, df)  — location_name 从第 0 行第 0 列提取（如"太华北路与红旗东路十字西-液位计"）
    """
    # 第 0 行第 0 列 = 位置标题
    df_raw = pd.read_excel(path, header=None, nrows=1)
    location_raw = str(df_raw.iloc[0, 0]) if not df_raw.empty else ""

    # 用第 1 行作列名，数据从第 2 行起
    df = pd.read_excel(path, header=1)
    return location_raw, df


def load_node_combined(path: Path) -> tuple[str | None, pd.DataFrame, pd.DataFrame]:
    """从新式节点 Excel 同时提取流量和液位两张表。

    Returns:
        (node_id, flow_df, level_df)  — node_id 可能为 None（未识别）
    """
    location_raw, df = _read_node_excel(path)

    # 时间戳：优先用"读取时间"（10min 对齐），否则找通用时间列
    ts_col = "读取时间" if "读取时间" in df.columns else _find_ts_column(df)
    if ts_col is None:
        raise ValueError(f"{path.name}: 未识别到时间戳列")
    ts = pd.to_datetime(df[ts_col], errors="coerce")

    # 构造一个带原始列名的 df 供 node_id 查找
    df_for_id = pd.DataFrame({location_raw: [None]})  # 把 location 放进"列名"供 _extract_node_id 读取

    node_id = _extract_node_id(path, df_for_id)

    # 液位表
    level_series = _pick_first(df, LEVEL_FIELD_ALIASES)
    level_df = pd.DataFrame()
    if level_series is not None and node_id is not None:
        level_df = pd.DataFrame({
            "node_id":  node_id,
            "ts":       ts,
            "level_m":  level_series,
            "qc_flag":  "good",
        }).dropna(subset=["ts"]).sort_values("ts").reset_index(drop=True)

    # 流量表
    flow_series = _pick_flow_with_unit(df)
    vel_series  = _pick_first(df, VELOCITY_FIELD_ALIASES)
    flow_df = pd.DataFrame()
    if flow_series is not None and node_id is not None:
        flow_df = pd.DataFrame({
            "node_id":    node_id,
            "ts":         ts,
            "flow_m3s":   flow_series,
            "velocity_ms": vel_series,
            "qc_flag":    "good",
        }).dropna(subset=["ts"]).sort_values("ts").reset_index(drop=True)

    return node_id, flow_df, level_df


# ---------------------------------------------------------------------------
# 旧式节点（nodes_flow / nodes_level）
# ---------------------------------------------------------------------------

def load_node_series(path: Path, kind: str) -> pd.DataFrame:
    """kind ∈ {nodes_flow, nodes_level}"""
    df = _read_any(path)
    tscol = _find_ts_column(df)
    if tscol is None:
        raise ValueError(f"{path.name}: 未识别到时间戳列")
    node_id = _extract_node_id(path, df)
    if node_id is None:
        raise ValueError(f"{path.name}: 未识别到 node_id（期望形如 S01 或 W13）")

    base = pd.DataFrame({
        "node_id": node_id,
        "ts": pd.to_datetime(df[tscol], errors="coerce"),
    })
    if kind == "nodes_level":
        base["level_m"] = _pick_first(df, LEVEL_FIELD_ALIASES)
    elif kind == "nodes_flow":
        base["flow_m3s"]    = _pick_flow_with_unit(df)
        base["velocity_ms"] = _pick_first(df, VELOCITY_FIELD_ALIASES)
    else:
        raise ValueError(kind)
    base["qc_flag"] = "good"
    base = base.dropna(subset=["ts"]).sort_values("ts").reset_index(drop=True)
    return base


# ---------------------------------------------------------------------------
# 雨量
# ---------------------------------------------------------------------------

def _is_meteo_format(df: pd.DataFrame) -> bool:
    """判断是否为气象局年月日时分列格式。"""
    return {"年", "月", "日", "时"}.issubset(set(df.columns))


def load_rainfall(path: Path) -> pd.DataFrame:
    df = _read_any(path)

    if _is_meteo_format(df):
        # 气象局格式：年/月/日/时 四列 → 合并为 datetime
        ts = pd.to_datetime(
            df["年"].astype(str) + "-" +
            df["月"].astype(str).str.zfill(2) + "-" +
            df["日"].astype(str).str.zfill(2) + " " +
            df["时"].astype(str).str.zfill(2) + ":00",
            errors="coerce",
        )
        # 区站号列
        sid_col = next(
            (c for c in df.columns if "区站号" in str(c) or "station" in str(c).lower()),
            None,
        )
        if sid_col is None:
            raise ValueError(f"{path.name}: 未识别到站点编号列（期望含'区站号'）")
        rain_series = _pick_first(df, RAIN_FIELD_ALIASES)
        out = pd.DataFrame({
            "station_id": df[sid_col].astype(str).str.strip(),
            "ts":          ts,
            "rain_mm_h":   rain_series,
        })
    else:
        # 通用格式：含时间戳列
        tscol = _find_ts_column(df)
        if tscol is None:
            raise ValueError(f"{path.name}: 未识别到时间戳列")
        sid = _extract_station_id(path, df)
        if sid is None:
            raise ValueError(f"{path.name}: 未识别到 station_id（期望含 V8805 等）")
        out = pd.DataFrame({
            "station_id": sid,
            "ts":         pd.to_datetime(df[tscol], errors="coerce"),
            "rain_mm_h":  _pick_first(df, RAIN_FIELD_ALIASES),
        })

    out["rain_mm_cum"] = out.groupby("station_id")["rain_mm_h"].cumsum()
    out["qc_flag"]     = "good"
    out = out.dropna(subset=["ts"]).sort_values(["station_id", "ts"]).reset_index(drop=True)
    return out


# ---------------------------------------------------------------------------
# 污水厂入流
# ---------------------------------------------------------------------------

def load_plant(path: Path) -> pd.DataFrame:
    df = _read_any(path)
    tscol = _find_ts_column(df)
    if tscol is None:
        raise ValueError(f"{path.name}: 未识别到时间戳列")
    out = pd.DataFrame({"ts": pd.to_datetime(df[tscol], errors="coerce")})
    for tgt, aliases in PLANT_FIELD_ALIASES.items():
        if tgt == "flow_m3s":
            out[tgt] = _pick_flow_with_unit(df)
        else:
            out[tgt] = _pick_first(df, aliases)
    out["qc_flag"] = "good"
    out = out.dropna(subset=["ts"]).sort_values("ts").reset_index(drop=True)
    return out


# ---------------------------------------------------------------------------
# Parquet upsert
# ---------------------------------------------------------------------------

DEDUPE_KEYS = {
    "plant_inlet_10min": ["ts"],
    "node_level_10min":  ["node_id", "ts"],
    "node_flow_10min":   ["node_id", "ts"],
    "rainfall_hourly":   ["station_id", "ts"],
}


def upsert_parquet(df: pd.DataFrame, kind: str) -> Path:
    """合并新数据到 parquet，按 DEDUPE_KEYS 去重（保留新值）。"""
    out_path = paths().parquet(kind)
    keys = DEDUPE_KEYS.get(kind)
    if not keys:
        raise ValueError(f"未知 kind：{kind}")
    if out_path.exists():
        prev = pd.read_parquet(out_path)
        combined = pd.concat([prev, df], ignore_index=True)
    else:
        combined = df.copy()
    combined = (combined
                .drop_duplicates(subset=keys, keep="last")
                .sort_values(keys)
                .reset_index(drop=True))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(out_path, index=False)
    return out_path


# ---------------------------------------------------------------------------
# 状态跟踪
# ---------------------------------------------------------------------------

def _load_state() -> dict:
    p = paths().ingest_state
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _save_state(state: dict) -> None:
    p = paths().ingest_state
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# 顶层入口
# ---------------------------------------------------------------------------

def run_ingest(*, force: bool = False) -> dict:
    """扫 raw → 解析 → upsert → 更新状态文件。返回每个 kind 的入库行数。"""
    state = _load_state()
    files = scan_raw()
    summary: dict[str, int] = {}

    for rf in files:
        prev = state.get(str(rf.path))
        if not force and prev and prev.get("sha256") == rf.sha256:
            continue

        try:
            if rf.kind == "plant_inlet":
                df = load_plant(rf.path)
                upsert_parquet(df, "plant_inlet_10min")
                summary["plant_inlet_10min"] = summary.get("plant_inlet_10min", 0) + len(df)

            elif rf.kind in {"nodes_sewage", "nodes_stormwater"}:
                node_id, flow_df, level_df = load_node_combined(rf.path)
                if node_id is None:
                    raise ValueError(
                        f"无法识别节点 ID，请确认文件名含规范 ID（如 W13）"
                        f"或位置名已登记在 sites.yaml 的 road / pinyin 字段中"
                    )
                if not level_df.empty:
                    upsert_parquet(level_df, "node_level_10min")
                    summary["node_level_10min"] = summary.get("node_level_10min", 0) + len(level_df)
                if not flow_df.empty:
                    upsert_parquet(flow_df, "node_flow_10min")
                    summary["node_flow_10min"] = summary.get("node_flow_10min", 0) + len(flow_df)

            elif rf.kind == "nodes_level":
                df = load_node_series(rf.path, "nodes_level")
                upsert_parquet(df, "node_level_10min")
                summary["node_level_10min"] = summary.get("node_level_10min", 0) + len(df)

            elif rf.kind == "nodes_flow":
                df = load_node_series(rf.path, "nodes_flow")
                upsert_parquet(df, "node_flow_10min")
                summary["node_flow_10min"] = summary.get("node_flow_10min", 0) + len(df)

            elif rf.kind == "rainfall":
                df = load_rainfall(rf.path)
                upsert_parquet(df, "rainfall_hourly")
                summary["rainfall_hourly"] = summary.get("rainfall_hourly", 0) + len(df)

        except Exception as e:  # noqa: BLE001
            state[str(rf.path)] = {"sha256": rf.sha256, "mtime": rf.mtime, "error": str(e)}
            continue

        state[str(rf.path)] = {"sha256": rf.sha256, "mtime": rf.mtime,
                                "rows": summary.get("node_level_10min", 0)}

    _save_state(state)
    return summary
