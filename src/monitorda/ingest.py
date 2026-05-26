"""数据接入：扫 data/raw/，识别文件类型与节点 ID，去重合并到 interim parquet。

不同来源平台的导出格式不统一，这里采用：
1. 文件路径分类（plant_inlet / nodes_flow / nodes_level / rainfall）
2. 文件名识别 node_id / station_id
3. 列名启发式匹配（settings.yaml: ingest.ts_column_candidates）
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .io_paths import paths, settings


# ---------------------------------------------------------------------------
# 文件扫描
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RawFile:
    path: Path
    kind: str  # plant_inlet | nodes_flow | nodes_level | rainfall
    sha256: str
    mtime: float


def scan_raw() -> list[RawFile]:
    """扫描 data/raw/ 下所有支持扩展名的文件。"""
    p = paths()
    accept = set(settings().get("ingest", {}).get("accept_extensions", [".csv", ".xlsx"]))
    items: list[RawFile] = []
    for kind, root in [
        ("plant_inlet", p.raw_plant),
        ("nodes_flow", p.raw_nodes_flow),
        ("nodes_level", p.raw_nodes_level),
        ("rainfall", p.raw_rainfall),
    ]:
        if not root.exists():
            continue
        for f in root.rglob("*"):
            if f.is_file() and f.suffix.lower() in accept and not f.name.startswith("."):
                items.append(RawFile(
                    path=f,
                    kind=kind,
                    sha256=_hash_file(f),
                    mtime=f.stat().st_mtime,
                ))
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
# 通用读取器
# ---------------------------------------------------------------------------

def _read_any(p: Path) -> pd.DataFrame:
    if p.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(p)
    # 文本：尝试若干编码
    for enc in ["utf-8", "utf-8-sig", "gbk", "gb18030"]:
        try:
            return pd.read_csv(p, encoding=enc)
        except UnicodeDecodeError:
            continue
    # 兜底
    return pd.read_csv(p, encoding="latin-1", on_bad_lines="skip")


def _find_ts_column(df: pd.DataFrame) -> str | None:
    candidates = settings().get("ingest", {}).get("ts_column_candidates", [])
    cols_lower = {c.lower(): c for c in df.columns.astype(str)}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    # 模糊匹配：列名包含 'time' 或 '时间'
    for col in df.columns:
        cl = str(col).lower()
        if "time" in cl or "时间" in str(col):
            return col
    return None


def _extract_node_id(path: Path, df: pd.DataFrame) -> str | None:
    """从文件名或表内列中匹配规范节点 ID。"""
    pat = settings().get("ingest", {}).get("node_id_pattern", r"(S0[1-9]|S10|W1[1-9])")
    m = re.search(pat, path.name)
    if m:
        return m.group(1)
    # 表内是否带 node_id 列
    for c in ["node_id", "节点", "节点编号", "site_id"]:
        if c in df.columns:
            vals = df[c].dropna().astype(str)
            for v in vals.head(20):
                m = re.search(pat, v)
                if m:
                    return m.group(1)
    return None


def _extract_station_id(path: Path, df: pd.DataFrame) -> str | None:
    m = re.search(r"(V\d{4,5})", path.name)
    if m:
        return m.group(1)
    for c in ["station_id", "雨量站", "station"]:
        if c in df.columns:
            vals = df[c].dropna().astype(str)
            for v in vals.head(20):
                m = re.search(r"(V\d{4,5})", v)
                if m:
                    return m.group(1)
    return None


# ---------------------------------------------------------------------------
# 字段映射 → 规范化 schema
# ---------------------------------------------------------------------------

PLANT_FIELD_ALIASES = {
    "flow_m3s": ["flow", "流量", "进水流量", "瞬时流量", "Q"],
    "ph": ["pH", "ph", "酸碱度"],
    "cod_mgL": ["COD", "cod", "化学需氧量"],
    "nh3n_mgL": ["NH3-N", "氨氮", "ammonia", "NH3N"],
    "temp_c": ["temp", "水温", "temperature"],
}

LEVEL_FIELD_ALIASES = ["level_m", "level", "液位", "水位", "depth"]
FLOW_FIELD_ALIASES = ["flow_m3s", "flow", "流量", "Q"]
VELOCITY_FIELD_ALIASES = ["velocity_ms", "velocity", "流速", "v"]
RAIN_FIELD_ALIASES = ["rain_mm_h", "rain", "降雨", "降水", "rainfall", "rain_mm"]


def _pick_first(df: pd.DataFrame, candidates: list[str]) -> pd.Series | None:
    for c in candidates:
        if c in df.columns:
            return pd.to_numeric(df[c], errors="coerce")
        for col in df.columns:
            if str(col).lower() == c.lower() or c.lower() in str(col).lower():
                return pd.to_numeric(df[col], errors="coerce")
    return None


# ---------------------------------------------------------------------------
# 解析每类文件
# ---------------------------------------------------------------------------

def load_plant(path: Path) -> pd.DataFrame:
    df = _read_any(path)
    tscol = _find_ts_column(df)
    if tscol is None:
        raise ValueError(f"{path.name}: 未识别到时间戳列")
    out = pd.DataFrame({"ts": pd.to_datetime(df[tscol], errors="coerce")})
    for tgt, aliases in PLANT_FIELD_ALIASES.items():
        out[tgt] = _pick_first(df, aliases)
    out["qc_flag"] = "good"
    out = out.dropna(subset=["ts"]).sort_values("ts").reset_index(drop=True)
    return out


def load_node_series(path: Path, kind: str) -> pd.DataFrame:
    """kind ∈ {nodes_flow, nodes_level}"""
    df = _read_any(path)
    tscol = _find_ts_column(df)
    if tscol is None:
        raise ValueError(f"{path.name}: 未识别到时间戳列")
    node_id = _extract_node_id(path, df)
    if node_id is None:
        raise ValueError(f"{path.name}: 未识别到 node_id（期望形如 S01–S10 或 W11–W19）")

    base = pd.DataFrame({
        "node_id": node_id,
        "ts": pd.to_datetime(df[tscol], errors="coerce"),
    })
    if kind == "nodes_level":
        base["level_m"] = _pick_first(df, LEVEL_FIELD_ALIASES)
    elif kind == "nodes_flow":
        base["flow_m3s"] = _pick_first(df, FLOW_FIELD_ALIASES)
        base["velocity_ms"] = _pick_first(df, VELOCITY_FIELD_ALIASES)
    else:
        raise ValueError(kind)
    base["qc_flag"] = "good"
    base = base.dropna(subset=["ts"]).sort_values("ts").reset_index(drop=True)
    return base


def load_rainfall(path: Path) -> pd.DataFrame:
    df = _read_any(path)
    tscol = _find_ts_column(df)
    if tscol is None:
        raise ValueError(f"{path.name}: 未识别到时间戳列")
    sid = _extract_station_id(path, df)
    if sid is None:
        raise ValueError(f"{path.name}: 未识别到 station_id（期望形如 V8805）")

    out = pd.DataFrame({
        "station_id": sid,
        "ts": pd.to_datetime(df[tscol], errors="coerce"),
        "rain_mm_h": _pick_first(df, RAIN_FIELD_ALIASES),
    })
    out["rain_mm_cum"] = out.groupby("station_id")["rain_mm_h"].cumsum()
    out["qc_flag"] = "good"
    out = out.dropna(subset=["ts"]).sort_values("ts").reset_index(drop=True)
    return out


# ---------------------------------------------------------------------------
# Parquet upsert
# ---------------------------------------------------------------------------

DEDUPE_KEYS = {
    "plant_inlet_10min": ["ts"],
    "node_level_10min": ["node_id", "ts"],
    "node_flow_10min": ["node_id", "ts"],
    "rainfall_hourly": ["station_id", "ts"],
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
    combined = combined.drop_duplicates(subset=keys, keep="last").sort_values(keys).reset_index(drop=True)
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

    kind_to_target = {
        "plant_inlet": "plant_inlet_10min",
        "nodes_flow": "node_flow_10min",
        "nodes_level": "node_level_10min",
        "rainfall": "rainfall_hourly",
    }

    for rf in files:
        prev = state.get(str(rf.path))
        if not force and prev and prev.get("sha256") == rf.sha256:
            continue
        try:
            if rf.kind == "plant_inlet":
                df = load_plant(rf.path)
            elif rf.kind in {"nodes_flow", "nodes_level"}:
                df = load_node_series(rf.path, rf.kind)
            elif rf.kind == "rainfall":
                df = load_rainfall(rf.path)
            else:
                continue
        except Exception as e:  # noqa: BLE001
            state[str(rf.path)] = {"sha256": rf.sha256, "mtime": rf.mtime, "error": str(e)}
            continue

        target = kind_to_target[rf.kind]
        upsert_parquet(df, target)
        summary[target] = summary.get(target, 0) + len(df)
        state[str(rf.path)] = {"sha256": rf.sha256, "mtime": rf.mtime, "rows": len(df)}

    _save_state(state)
    return summary
