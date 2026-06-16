"""夜间最小液位（NML）分析 — 量化持续性背景入渗。

方法来源：
  EPA Night Minimum Flow (NMF) method
  参考：WEF MOP 60 §7.4、T/CECS 1764-2024《城镇污水管网入流入渗监测与评估标准》

原理：
  凌晨 02:00–04:00 居民用水量可忽略，此窗口的最低液位（Night Minimum Level, NML）
  可视为该时刻管网内"背景入渗底线"的代用指标。

输出两张表：
  nmf_by_node    逐日逐节点 NML 时序（可用于时间趋势图）
  nmf_summary    节点级汇总 + NMFD 指标

NMFD（Night Minimum Flow Deviation）：
  nmfd_ratio = (NML_雨后 - NML_旱夜) / NML_旱夜
  越高 → 降雨后地下水位抬升越明显 → 入渗贡献越大
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 参数
# ---------------------------------------------------------------------------

_NIGHT_START_H = 2    # 凌晨 02:00
_NIGHT_END_H   = 4    # 凌晨 04:00（不含）
_MIN_POINTS    = 2    # 夜间窗口内至少 2 个有效点（实测约 1–3 点/2h，非严格 10min 等间隔）
_DRY_RAIN_THRESH_MM  = 1.0   # 前 24h 降雨量低于此值视为旱夜
_POST_RAIN_MIN_H     = 12    # 事件结束后至少 12h（地下水响应延迟）
_POST_RAIN_MAX_H     = 96    # 事件结束后最多 96h（之后归为旱夜恢复）
_MIN_EVENT_RAIN_MM   = 5.0   # 触发"雨后"标注的最低事件雨量


@dataclass
class NMFResult:
    node_id: str
    n_dry_nights: int
    n_post_nights: int
    nml_dry_m: float | None        # 旱夜 NML 中位数（m）
    nml_post_m: float | None       # 雨后 NML 中位数（m）
    nmfd_ratio: float | None       # (post - dry) / dry
    nmfd_abs_m: float | None       # post - dry（绝对抬升量，m）
    category_nmfd: str  # high_infiltration / moderate / low / negative_response / no_post_data / data_insufficient


# ---------------------------------------------------------------------------
# 核心：逐日 NML 计算
# ---------------------------------------------------------------------------

def _night_window_dates(level_series: pd.Series) -> pd.DatetimeIndex:
    """返回数据覆盖范围内的每一天日期。"""
    if level_series.empty:
        return pd.DatetimeIndex([])
    d_start = level_series.index.min().normalize()
    d_end   = level_series.index.max().normalize()
    return pd.date_range(d_start, d_end, freq="D")


def compute_nml_series(
    node_id: str,
    level_series: pd.Series,          # DatetimeIndex 10min, good-only
    rain_series_dict: dict[str, pd.Series],  # station → hourly rain
    events_df: pd.DataFrame,
    station_id: str | None = None,
) -> pd.DataFrame:
    """对单节点计算逐日 NML，标注旱夜 / 雨后夜。

    Returns
    -------
    DataFrame with columns:
        date, node_id, nml_m, n_points, is_dry, is_post_rain,
        rain_prev24h_mm, hours_since_event_end
    """
    dates = _night_window_dates(level_series)
    if len(dates) == 0:
        return pd.DataFrame()

    # 降雨序列：选站（优先 station_id；否则取各站最大值）
    rain_avail = list(rain_series_dict.keys())
    if not rain_avail:
        rain_combined: pd.Series = pd.Series(dtype=float)
    else:
        sids = [station_id] if station_id and station_id in rain_series_dict else rain_avail
        rain_frames = [rain_series_dict[s] for s in sids]
        rain_combined = pd.concat(rain_frames, axis=1).max(axis=1).sort_index()
        # 补全缺失小时为 0（无记录 = 无雨）
        if not rain_combined.empty:
            full_h = pd.date_range(rain_combined.index.min(),
                                   rain_combined.index.max(), freq="h")
            rain_combined = rain_combined.reindex(full_h, fill_value=0.0)

    # 事件结束时间列表（雨量足够的事件）
    event_ends: list[pd.Timestamp] = []
    if not events_df.empty:
        for _, ev in events_df.iterrows():
            if float(ev.get("total_mm", 0)) >= _MIN_EVENT_RAIN_MM:
                event_ends.append(pd.Timestamp(ev["t_end"]))

    rows = []
    for d in dates:
        # 夜间窗口：当天 02:00–04:00
        t0 = d + pd.Timedelta(hours=_NIGHT_START_H)
        t1 = d + pd.Timedelta(hours=_NIGHT_END_H)

        # 提取有效液位点
        win = level_series.loc[t0:t1]
        win_valid = win.dropna()
        n_pts = len(win_valid)
        nml = float(win_valid.min()) if n_pts >= _MIN_POINTS else np.nan

        # 前 24h 降雨量
        rain_24h = 0.0
        if not rain_combined.empty:
            t_rain_start = t0 - pd.Timedelta(hours=24)
            rain_win = rain_combined.loc[t_rain_start:t0]
            rain_24h = float(rain_win.sum()) if not rain_win.empty else 0.0

        # 距最近事件结束的时长
        hours_since_end = np.nan
        if event_ends:
            diffs = [(t0 - te).total_seconds() / 3600 for te in event_ends]
            pos_diffs = [x for x in diffs if x >= 0]
            if pos_diffs:
                hours_since_end = min(pos_diffs)

        is_dry = (rain_24h < _DRY_RAIN_THRESH_MM) and (
            np.isnan(hours_since_end) or hours_since_end > _POST_RAIN_MAX_H
        )
        is_post = (
            not np.isnan(hours_since_end)
            and _POST_RAIN_MIN_H <= hours_since_end <= _POST_RAIN_MAX_H
        )

        rows.append({
            "date":               d.date(),
            "node_id":            node_id,
            "nml_m":              nml,
            "n_points":           n_pts,
            "is_dry":             is_dry,
            "is_post_rain":       is_post,
            "rain_prev24h_mm":    rain_24h,
            "hours_since_event_end": hours_since_end,
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 节点级汇总
# ---------------------------------------------------------------------------

def summarize_node(node_id: str, daily_df: pd.DataFrame) -> NMFResult:
    """从逐日 NML 表计算节点级汇总指标。"""
    no_data = NMFResult(
        node_id=node_id, n_dry_nights=0, n_post_nights=0,
        nml_dry_m=None, nml_post_m=None,
        nmfd_ratio=None, nmfd_abs_m=None,
        category_nmfd="data_insufficient",
    )
    if daily_df.empty:
        return no_data

    valid = daily_df.dropna(subset=["nml_m"])
    dry   = valid[valid["is_dry"]]
    post  = valid[valid["is_post_rain"]]

    n_dry  = len(dry)
    n_post = len(post)

    nml_dry  = float(dry["nml_m"].median())  if n_dry  >= 2 else None
    nml_post = float(post["nml_m"].median()) if n_post >= 1 else None

    nmfd_ratio = None
    nmfd_abs   = None
    if nml_dry is not None and nml_post is not None and nml_dry > 1e-6:
        nmfd_abs   = nml_post - nml_dry
        nmfd_ratio = nmfd_abs / nml_dry

    # 分类
    if n_dry < 2:
        cat = "data_insufficient"
    elif n_post < 1:
        # 有旱夜数据但无雨后夜数据（事件期间设备离线或无覆盖）
        cat = "no_post_data"
    elif nmfd_ratio is None:
        cat = "data_insufficient"
    elif nmfd_ratio < -0.10:
        # 雨后 NML 低于旱夜基线：液位计数据的水力效应（回落段），非入渗减少
        cat = "negative_response"
    elif nmfd_ratio >= 0.30:
        cat = "high_infiltration"   # 雨后 NML 较旱夜抬升 ≥30%，地下水入渗显著
    elif nmfd_ratio >= 0.10:
        cat = "moderate"
    else:
        cat = "low"

    return NMFResult(
        node_id=node_id,
        n_dry_nights=n_dry,
        n_post_nights=n_post,
        nml_dry_m=nml_dry,
        nml_post_m=nml_post,
        nmfd_ratio=nmfd_ratio,
        nmfd_abs_m=nmfd_abs,
        category_nmfd=cat,
    )


# ---------------------------------------------------------------------------
# 管线入口
# ---------------------------------------------------------------------------

def run_nmf() -> tuple[pd.DataFrame, pd.DataFrame]:
    """读取 interim parquet → 对所有污水节点计算 NMF → 写两张 parquet。

    Returns
    -------
    (daily_df, summary_df)
    """
    from .io_paths import paths, sites
    from .spatial import station_for_node

    p = paths()

    for required in ("node_level_10min", "rainfall_hourly", "events"):
        src = p.parquet(required)
        if not src.exists():
            raise FileNotFoundError(f"找不到 {src}，请先运行上游 stage")

    lv_all   = pd.read_parquet(p.parquet("node_level_10min"))
    rain_all = pd.read_parquet(p.parquet("rainfall_hourly"))
    events_df = pd.read_parquet(p.parquet("events"))

    # 降雨 → dict[station_id → Series]
    rain_dict: dict[str, pd.Series] = {}
    for sid, grp in rain_all.groupby("station_id"):
        rain_dict[str(sid)] = grp.set_index("ts")["rain_mm_h"].sort_index()

    # 仅污水节点
    site_cfg = sites().get("nodes") or {}
    node_ids = sorted(nid for nid, cfg in site_cfg.items() if cfg.get("kind") == "sewage")

    daily_rows: list[pd.DataFrame] = []
    summary_rows: list[dict] = []

    for nid in node_ids:
        lv_node = (
            lv_all[(lv_all["node_id"] == nid) & (lv_all["qc_flag"] == "good")]
            .set_index("ts")["level_m"]
            .sort_index()
        )
        sid = station_for_node(nid)
        daily = compute_nml_series(nid, lv_node, rain_dict, events_df, station_id=sid)
        if not daily.empty:
            daily_rows.append(daily)

        summary = summarize_node(nid, daily)
        summary_rows.append({
            "node_id":        summary.node_id,
            "n_dry_nights":   summary.n_dry_nights,
            "n_post_nights":  summary.n_post_nights,
            "nml_dry_m":      summary.nml_dry_m,
            "nml_post_m":     summary.nml_post_m,
            "nmfd_ratio":     summary.nmfd_ratio,
            "nmfd_abs_m":     summary.nmfd_abs_m,
            "category_nmfd":  summary.category_nmfd,
        })

    daily_df   = pd.concat(daily_rows, ignore_index=True) if daily_rows else pd.DataFrame()
    summary_df = pd.DataFrame(summary_rows).sort_values("node_id").reset_index(drop=True)

    # 写出
    out_daily   = p.parquet("nmf_by_node")
    out_summary = p.parquet("nmf_summary")
    if not daily_df.empty:
        daily_df.to_parquet(out_daily, index=False)
    summary_df.to_parquet(out_summary, index=False)

    return daily_df, summary_df
