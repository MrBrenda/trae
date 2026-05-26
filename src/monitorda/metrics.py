"""方法论核心：BWF / RDII / Qrl / 等效混接面积 / 时滞 / 回落半衰期。

所有函数都是纯函数（pandas + numpy），便于单元测试与回归验证。
方法论来源：《红旗东路积涝整治及管网改造专题研究阶段性成果报告 0423》。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 数据契约
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EventWindow:
    """单场降雨事件的时间窗。"""
    event_id: str
    t_start: pd.Timestamp
    t_end: pd.Timestamp        # 降雨结束时刻（不含 recession tail）
    total_mm: float            # 事件累计降雨


# ---------------------------------------------------------------------------
# 旱天基线 BWF
# ---------------------------------------------------------------------------

def bwf(
    series: pd.Series,
    event: EventWindow,
    *,
    window_days: int = 14,
    exclude_radius_h: float = 48.0,
    other_events: list[EventWindow] | None = None,
    estimator: str = "median",
    min_samples: int = 144,
) -> tuple[float | None, pd.Timestamp, pd.Timestamp, int]:
    """计算事件前后 ±window_days 的旱天基线。

    Parameters
    ----------
    series : pd.Series
        以时间为索引（DatetimeIndex）的流量或液位序列。
    event : EventWindow
        当前事件。
    window_days : int
        事件前后各取 N 天作为旱天候选窗。
    exclude_radius_h : float
        旱天候选窗内排除任一事件 ±N 小时附近的数据。
    other_events : list[EventWindow] | None
        其它事件，用于把它们的影响段也排除掉。
    estimator : {"median", "mean", "trimmed_mean"}
        基线估计量。
    min_samples : int
        样本数不足则返回 None（窗口不可信）。

    Returns
    -------
    baseline : float | None
    window_start, window_end : pd.Timestamp
    n_samples : int
    """
    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError("series 必须使用 DatetimeIndex")

    win_start = event.t_start - timedelta(days=window_days)
    win_end = event.t_end + timedelta(days=window_days)
    window = series.loc[win_start:win_end].copy()

    # 排除当前事件 + recession tail
    excl_start = event.t_start - timedelta(hours=exclude_radius_h)
    excl_end = event.t_end + timedelta(hours=exclude_radius_h)
    mask = (window.index < excl_start) | (window.index > excl_end)
    window = window[mask]

    # 排除其它事件
    for ev in other_events or []:
        if ev.event_id == event.event_id:
            continue
        s = ev.t_start - timedelta(hours=exclude_radius_h)
        e = ev.t_end + timedelta(hours=exclude_radius_h)
        window = window[(window.index < s) | (window.index > e)]

    window = window.dropna()
    n = int(window.shape[0])
    if n < min_samples:
        return None, win_start, win_end, n

    if estimator == "median":
        b = float(window.median())
    elif estimator == "mean":
        b = float(window.mean())
    elif estimator == "trimmed_mean":
        lo, hi = window.quantile([0.05, 0.95])
        b = float(window[(window >= lo) & (window <= hi)].mean())
    else:
        raise ValueError(f"未知 estimator：{estimator}")

    return b, win_start, win_end, n


# ---------------------------------------------------------------------------
# RDII
# ---------------------------------------------------------------------------

def rdii(
    series: pd.Series,
    event: EventWindow,
    baseline: float,
    *,
    recession_tail_h: float = 48.0,
) -> tuple[float | None, float | None]:
    """事件期 + recession tail 内 流量超 BWF 的累计体积。

    Returns
    -------
    v_rdii_m3 : 累计体积（立方米）。series 单位为 m³/s。
    rdii_peak_m3s : 期间内最大超基线流量。
    """
    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError("series 必须使用 DatetimeIndex")
    if baseline is None or np.isnan(baseline):
        return None, None

    end_with_tail = event.t_end + timedelta(hours=recession_tail_h)
    win = series.loc[event.t_start:end_with_tail].dropna()
    if win.empty:
        return None, None

    delta = (win - baseline).clip(lower=0.0)
    if delta.empty:
        return 0.0, 0.0

    # 数值梯形积分；时间步可能不等间距
    t_sec = (win.index.to_series().diff().dt.total_seconds()
             .bfill().ffill()).to_numpy()
    # 采用中间值法：每段用左右值平均
    vals = delta.to_numpy()
    if len(vals) < 2:
        # 单点：用当前间隔默认 600s（10 分钟采样）
        return float(vals[0] * 600.0), float(vals[0])

    midvals = (vals[:-1] + vals[1:]) / 2.0
    seg_sec = t_sec[1:]
    v = float((midvals * seg_sec).sum())
    return v, float(delta.max())


# ---------------------------------------------------------------------------
# 等效混接面积
# ---------------------------------------------------------------------------

def equivalent_illicit_area(
    v_rdii_m3: float | None,
    rainfall_mm: float,
    runoff_coeff: float,
) -> float | None:
    """等效混接面积 km²
    A = V_RDII / (C × P × 1000)
    其中 P 单位 mm，V 单位 m³。
    """
    if v_rdii_m3 is None or np.isnan(v_rdii_m3):
        return None
    if rainfall_mm <= 0 or runoff_coeff <= 0:
        return None
    return float(v_rdii_m3 / (runoff_coeff * rainfall_mm * 1000.0))


# ---------------------------------------------------------------------------
# Qrl 雨水入流评定值
# ---------------------------------------------------------------------------

def qrl(
    rdii_volumes: list[float],
    rainfalls_mm: list[float],
    pipe_lengths_km: list[float],
) -> float | None:
    """Qrl = Σ(RDII_j / R_j) / Σ(L_i)   单位 m³/(km·mm)

    对应原报告"雨水入流评定值"，跨事件、跨节点归一化。
    """
    pairs = [(v, r) for v, r in zip(rdii_volumes, rainfalls_mm)
             if v is not None and r is not None and r > 0 and not np.isnan(v)]
    if not pairs:
        return None
    total_pipe = float(sum(L for L in pipe_lengths_km if L and L > 0))
    if total_pipe <= 0:
        return None
    numer = float(sum(v / r for v, r in pairs))
    return numer / total_pipe


# ---------------------------------------------------------------------------
# 液位升幅 / 时滞
# ---------------------------------------------------------------------------

def rise_amp(
    level_series: pd.Series,
    event: EventWindow,
    baseline_level: float,
    *,
    recession_tail_h: float = 48.0,
) -> float | None:
    """事件期间液位最大值 - BWF 液位基线。"""
    if baseline_level is None or np.isnan(baseline_level):
        return None
    end = event.t_end + timedelta(hours=recession_tail_h)
    win = level_series.loc[event.t_start:end].dropna()
    if win.empty:
        return None
    return float(win.max() - baseline_level)


def lag_start(
    response_series: pd.Series,
    rain_t_start: pd.Timestamp,
    baseline: float,
    *,
    rise_threshold: float = 0.05,
    lag_max_hours: float = 24.0,
) -> float | None:
    """起始时滞（小时）：响应序列首次超过 baseline + rise_threshold 的时刻 - rain_t_start。"""
    if baseline is None or np.isnan(baseline):
        return None
    end = rain_t_start + timedelta(hours=lag_max_hours)
    win = response_series.loc[rain_t_start:end].dropna()
    above = win[win > baseline + rise_threshold]
    if above.empty:
        return None
    return float((above.index[0] - rain_t_start).total_seconds() / 3600.0)


def lag_peak(
    response_series: pd.Series,
    rain_t_start: pd.Timestamp,
    event_t_end: pd.Timestamp,
    *,
    recession_tail_h: float = 48.0,
) -> float | None:
    """峰值时滞（小时）：响应峰值时刻 - rain_t_start。"""
    end = event_t_end + timedelta(hours=recession_tail_h)
    win = response_series.loc[rain_t_start:end].dropna()
    if win.empty:
        return None
    peak_t = win.idxmax()
    return float((peak_t - rain_t_start).total_seconds() / 3600.0)


# ---------------------------------------------------------------------------
# 回落半衰期
# ---------------------------------------------------------------------------

def recession_halflife(
    response_series: pd.Series,
    event_t_end: pd.Timestamp,
    baseline: float,
    *,
    fit_window_h: float = 48.0,
) -> float | None:
    """对事件结束后的回落段做一阶指数拟合：
        y(t) - b ≈ A * exp(-t / τ)
    半衰期 t_half = τ · ln(2)。

    返回小时；拟合失败或衰减过弱时返回 None。
    """
    if baseline is None or np.isnan(baseline):
        return None
    end = event_t_end + timedelta(hours=fit_window_h)
    seg = response_series.loc[event_t_end:end].dropna()
    if len(seg) < 6:
        return None

    y = seg.to_numpy() - baseline
    # 只对正值段拟合
    pos = y > 0
    if pos.sum() < 6:
        return None
    y = y[pos]
    t_h = (seg.index[pos] - seg.index[0]).total_seconds().to_numpy() / 3600.0

    try:
        coeffs = np.polyfit(t_h, np.log(y), 1)
    except (np.linalg.LinAlgError, ValueError):
        return None
    slope = float(coeffs[0])
    if slope >= 0:  # 没有衰减
        return None
    tau = -1.0 / slope
    return float(tau * np.log(2.0))


# ---------------------------------------------------------------------------
# 流量 ⇆ 液位 一致性
# ---------------------------------------------------------------------------

def qv_a_consistency(
    flow_m3s: float,
    velocity_ms: float | None,
    cross_section_area_m2: float,
    tolerance: float = 0.25,
) -> bool:
    """Q = v × A 是否在容差内一致。velocity 缺失时直接返回 True（无法判断）。"""
    if velocity_ms is None or np.isnan(velocity_ms):
        return True
    expected = velocity_ms * cross_section_area_m2
    if expected == 0:
        return flow_m3s == 0
    return abs(flow_m3s - expected) / abs(expected) <= tolerance
