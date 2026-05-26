"""降雨事件自动识别。"""

from __future__ import annotations

from datetime import timedelta

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
    """从小时级降雨中识别事件。

    Parameters
    ----------
    rain_hourly : DataFrame with columns ['station_id', 'ts', 'rain_mm_h']
    其他参数见 config/settings.yaml#events。

    Returns
    -------
    events : DataFrame with columns
        ['event_id', 'station_id', 't_start', 't_peak', 't_end',
         'duration_h', 'total_mm', 'max_intensity_mmh',
         'antecedent_dry_d', 'compound']
    """
    required = {"station_id", "ts", "rain_mm_h"}
    missing = required - set(rain_hourly.columns)
    if missing:
        raise ValueError(f"rain_hourly 缺少列：{missing}")

    out_rows: list[dict] = []
    for sid, sub in rain_hourly.groupby("station_id"):
        sub = sub.sort_values("ts").reset_index(drop=True)
        events = _detect_for_station(
            sub,
            wet_hour_threshold_mm=wet_hour_threshold_mm,
            min_event_total_mm=min_event_total_mm,
            min_event_duration_h=min_event_duration_h,
            internal_dry_gap_h=internal_dry_gap_h,
            merge_gap_h=merge_gap_h,
            merge_gap_mm=merge_gap_mm,
        )
        for ev in events:
            ev["station_id"] = sid
            ev["event_id"] = f"E{ev['t_start'].strftime('%Y%m%d')}-{sid}"
            out_rows.append(ev)

    if not out_rows:
        return pd.DataFrame(columns=[
            "event_id", "station_id", "t_start", "t_peak", "t_end",
            "duration_h", "total_mm", "max_intensity_mmh",
            "antecedent_dry_d", "compound",
        ])

    df = pd.DataFrame(out_rows).sort_values(["station_id", "t_start"]).reset_index(drop=True)
    df = _annotate_antecedent_dry(df, rain_hourly, antecedent_dry_h=antecedent_dry_h)
    # 列序整理
    df = df[[
        "event_id", "station_id", "t_start", "t_peak", "t_end",
        "duration_h", "total_mm", "max_intensity_mmh",
        "antecedent_dry_d", "compound",
    ]]
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


def _annotate_antecedent_dry(
    events: pd.DataFrame,
    rain_hourly: pd.DataFrame,
    *,
    antecedent_dry_h: float,
) -> pd.DataFrame:
    events = events.copy()
    dry_h_list: list[float | None] = []
    compound_list: list[bool] = []
    for _, ev in events.iterrows():
        sub = rain_hourly[(rain_hourly["station_id"] == ev["station_id"])
                          & (rain_hourly["ts"] < ev["t_start"])]
        if sub.empty:
            dry_h_list.append(None)
            compound_list.append(False)
            continue
        sub = sub.sort_values("ts")
        # 从 t_start 向前找最后一个 wet hour
        wet = sub[sub["rain_mm_h"].fillna(0) > 0]
        if wet.empty:
            dry_h_list.append(None)
            compound_list.append(False)
            continue
        gap = (ev["t_start"] - wet["ts"].iloc[-1]).total_seconds() / 3600.0
        dry_h_list.append(float(gap) / 24.0)  # 转天
        compound_list.append(gap < antecedent_dry_h)
    events["antecedent_dry_d"] = dry_h_list
    events["compound"] = compound_list
    return events
