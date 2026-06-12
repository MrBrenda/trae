"""降雨事件自动识别。

识别逻辑：
1. 按雨量站逐站识别降雨段（wet run → 合并 → 阈值筛选）
2. 跨站合并：时间窗口重叠或间隔 < merge_gap_h 的不同站次事件合并为同一场次
3. 统一事件 ID 按时序编号：E{YYYYMMDD}-{seq:02d}
4. station_id 保留降雨量最大的"代表站"，n_stations 记录参与该场次的站数

注：后期可基于 Thiessen 多边形对不同节点分配空间权重降雨，目前全区统一用代表站。
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def detect_events(
    rain_hourly: pd.DataFrame,
    *,
    wet_hour_threshold_mm: float = 0.5,
    min_event_total_mm: float = 2.0,
    min_event_duration_h: float = 2.0,
    internal_dry_gap_h: float = 3.0,
    merge_gap_h: float = 6.0,
    merge_gap_mm: float = 1.0,
    antecedent_dry_h: float = 24.0,
) -> pd.DataFrame:
    """从小时级降雨中识别统一降雨事件。

    Parameters
    ----------
    rain_hourly : DataFrame with columns ['station_id', 'ts', 'rain_mm_h']
    其他参数见 config/settings.yaml#events。

    Returns
    -------
    events : DataFrame，每行对应一场统一降雨事件，columns：
        event_id, station_id（代表站）, n_stations（参与站数）,
        t_start, t_peak, t_end, duration_h, total_mm, max_intensity_mmh,
        antecedent_dry_d, compound
    """
    required = {"station_id", "ts", "rain_mm_h"}
    missing = required - set(rain_hourly.columns)
    if missing:
        raise ValueError(f"rain_hourly 缺少列：{missing}")

    # 第一步：逐站识别
    per_station: list[dict] = []
    for sid, sub in rain_hourly.groupby("station_id"):
        sub = sub.sort_values("ts").reset_index(drop=True)
        for ev in _detect_for_station(
            sub,
            wet_hour_threshold_mm=wet_hour_threshold_mm,
            min_event_total_mm=min_event_total_mm,
            min_event_duration_h=min_event_duration_h,
            internal_dry_gap_h=internal_dry_gap_h,
            merge_gap_h=merge_gap_h,
            merge_gap_mm=merge_gap_mm,
        ):
            ev["station_id"] = sid
            per_station.append(ev)

    if not per_station:
        return pd.DataFrame(columns=[
            "event_id", "station_id", "n_stations", "t_start", "t_peak", "t_end",
            "duration_h", "total_mm", "max_intensity_mmh", "antecedent_dry_d", "compound",
        ])

    # 第二步：跨站时间合并
    unified = _unify_across_stations(per_station, merge_gap_h=merge_gap_h)

    # 第三步：排序 + 编号
    df = pd.DataFrame(unified).sort_values("t_start").reset_index(drop=True)
    df = _assign_event_ids(df)
    df = _annotate_antecedent_dry_unified(df, rain_hourly, antecedent_dry_h=antecedent_dry_h)

    return df[[
        "event_id", "station_id", "n_stations", "t_start", "t_peak", "t_end",
        "duration_h", "total_mm", "max_intensity_mmh", "antecedent_dry_d", "compound",
    ]]


# ---------------------------------------------------------------------------
# 跨站合并
# ---------------------------------------------------------------------------

def _unify_across_stations(per_station: list[dict], *, merge_gap_h: float) -> list[dict]:
    """将不同站的事件按时间窗口合并为统一场次。"""
    rows = sorted(per_station, key=lambda r: r["t_start"])

    groups: list[tuple[pd.Timestamp, pd.Timestamp, list[dict]]] = []
    for row in rows:
        if not groups:
            groups.append((row["t_start"], row["t_end"], [row]))
            continue
        g_start, g_end, members = groups[-1]
        gap_h = (row["t_start"] - g_end).total_seconds() / 3600.0
        if gap_h <= merge_gap_h:
            new_end = max(g_end, row["t_end"])
            groups[-1] = (g_start, new_end, members + [row])
        else:
            groups.append((row["t_start"], row["t_end"], [row]))

    result = []
    for t_start, t_end, members in groups:
        dominant = max(members, key=lambda m: m.get("total_mm", 0.0))
        stations = {m["station_id"] for m in members}
        duration_h = (t_end - t_start).total_seconds() / 3600.0 + 1.0
        result.append({
            "t_start":          t_start,
            "t_end":            t_end,
            "t_peak":           dominant["t_peak"],
            "station_id":       dominant["station_id"],
            "n_stations":       len(stations),
            "total_mm":         max(m.get("total_mm", 0.0) for m in members),
            "max_intensity_mmh": max(m.get("max_intensity_mmh", 0.0) for m in members),
            "duration_h":       duration_h,
        })
    return result


def _assign_event_ids(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    ids, date_seq = [], {}
    for _, row in df.iterrows():
        d = row["t_start"].strftime("%Y%m%d")
        seq = date_seq.get(d, 0) + 1
        date_seq[d] = seq
        ids.append(f"E{d}-{seq:02d}")
    df["event_id"] = ids
    return df


def _detect_for_station(
    sub: pd.DataFrame,
    *,
    wet_hour_threshold_mm: float,
    min_event_total_mm: float,
    min_event_duration_h: float,
    internal_dry_gap_h: float,
    merge_gap_h: float,
    merge_gap_mm: float,
) -> list[dict]:
    ts = sub["ts"].to_numpy()
    rain = sub["rain_mm_h"].fillna(0).to_numpy()
    wet = rain >= wet_hour_threshold_mm

    # 第一阶段：找连续 wet run，允许内部 ≤ internal_dry_gap_h 干口
    # 注意：数据是稀疏的（只记录有雨时刻），连续行之间可能存在大时间跳跃。
    # 必须同时检查时间距离，避免将跨越长期无记录期的两次降雨合并入同一 run。
    raw_runs: list[tuple[int, int]] = []
    i = 0
    n = len(rain)
    while i < n:
        if not wet[i]:
            i += 1
            continue
        j = i
        last_wet = i
        while j + 1 < n:
            gap_h = _hours_between(ts[last_wet], ts[j + 1])
            # 若距上次湿润时刻超过 merge_gap_h，无论下一行是否为湿润均视为新 run
            if gap_h > merge_gap_h:
                break
            if wet[j + 1]:
                last_wet = j + 1
                j += 1
            elif gap_h <= internal_dry_gap_h:
                # 允许跨越短暂干口
                j += 1
            else:
                break
        # run 截断到最后一个 wet hour
        raw_runs.append((i, last_wet))
        i = last_wet + 1

    # 第二阶段：合并相邻 run（< merge_gap_h，间隙降雨 < merge_gap_mm）
    merged: list[tuple[int, int]] = []
    for run in raw_runs:
        if not merged:
            merged.append(run)
            continue
        prev = merged[-1]
        gap_h = _hours_between(ts[prev[1]], ts[run[0]])
        gap_rain = float(rain[prev[1] + 1:run[0]].sum())
        if gap_h < merge_gap_h and gap_rain < merge_gap_mm:
            merged[-1] = (prev[0], run[1])
        else:
            merged.append(run)

    # 第三阶段：筛阈值
    events: list[dict] = []
    for (a, b) in merged:
        seg_rain = rain[a:b + 1]
        total = float(seg_rain.sum())
        dur_h = _hours_between(ts[a], ts[b]) + 1.0  # +1 因为小时分桶包含两端
        if total < min_event_total_mm or dur_h < min_event_duration_h:
            continue
        peak_idx = a + int(np.argmax(seg_rain))
        events.append({
            "t_start": pd.Timestamp(ts[a]),
            "t_end": pd.Timestamp(ts[b]),
            "t_peak": pd.Timestamp(ts[peak_idx]),
            "duration_h": float(dur_h),
            "total_mm": total,
            "max_intensity_mmh": float(seg_rain.max()),
        })
    return events


def _hours_between(a, b) -> float:
    a = pd.Timestamp(a)
    b = pd.Timestamp(b)
    return (b - a).total_seconds() / 3600.0


def _annotate_antecedent_dry_unified(
    events: pd.DataFrame,
    rain_hourly: pd.DataFrame,
    *,
    antecedent_dry_h: float,
) -> pd.DataFrame:
    """按代表站向前查找前期干旱时长。"""
    events = events.copy()
    dry_list, compound_list = [], []
    for _, ev in events.iterrows():
        sub = rain_hourly[
            (rain_hourly["station_id"] == ev["station_id"]) &
            (rain_hourly["ts"] < ev["t_start"])
        ].sort_values("ts")
        wet = sub[sub["rain_mm_h"].fillna(0) > 0]
        if wet.empty:
            dry_list.append(None)
            compound_list.append(False)
        else:
            gap_h = (ev["t_start"] - wet["ts"].iloc[-1]).total_seconds() / 3600.0
            dry_list.append(gap_h / 24.0)
            compound_list.append(gap_h < antecedent_dry_h)
    events["antecedent_dry_d"] = dry_list
    events["compound"] = compound_list
    return events
