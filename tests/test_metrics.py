"""metrics 模块的闭式合成数据单元测试。"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from monitorda.metrics import (
    EventWindow,
    bwf,
    equivalent_illicit_area,
    lag_peak,
    lag_start,
    qrl,
    qv_a_consistency,
    rdii,
    recession_halflife,
    rise_amp,
)


def _make_series(values, freq_min=10, start="2025-06-01 00:00:00"):
    idx = pd.date_range(start, periods=len(values), freq=f"{freq_min}min")
    return pd.Series(values, index=idx)


# ---------------------------------------------------------------------------
# BWF
# ---------------------------------------------------------------------------

def test_bwf_median_of_dry_baseline():
    # 28 天 ± 事件，全为 dry baseline = 0.5；事件 1 天值 = 5（应被排除）
    n_days = 30
    minutes_per_day = 24 * 6  # 10min
    base = np.full(n_days * minutes_per_day, 0.5)
    s = _make_series(base, freq_min=10, start="2025-06-01")
    # 事件在第 15 天 00:00 - 23:50
    t_start = s.index[14 * minutes_per_day]
    t_end = s.index[15 * minutes_per_day - 1]
    # 让事件期数值变高（应被排除）
    mask = (s.index >= t_start) & (s.index <= t_end)
    s[mask] = 5.0

    ev = EventWindow("E1", t_start, t_end, total_mm=10)
    b, ws, we, n = bwf(s, ev, window_days=14, exclude_radius_h=48, min_samples=10)
    assert b is not None
    assert b == pytest.approx(0.5, abs=1e-6)
    assert n > 0


def test_bwf_returns_none_when_too_few_samples():
    s = _make_series([0.5] * 5, freq_min=10)
    ev = EventWindow("E1", s.index[0], s.index[4], total_mm=10)
    b, _, _, n = bwf(s, ev, window_days=14, min_samples=144)
    assert b is None


# ---------------------------------------------------------------------------
# RDII
# ---------------------------------------------------------------------------

def test_rdii_volume_constant_excess():
    """事件期 baseline=0.5，每秒超出 1.0 m³/s，2 小时 → V = 1 * 7200 = 7200 m³"""
    # 100 个点的 baseline + 在事件期注入 1.0 超量
    n = 200
    s_vals = np.full(n, 0.5)
    idx = pd.date_range("2025-06-01", periods=n, freq="60s")  # 1秒采样太慢，60s
    s = pd.Series(s_vals, index=idx)
    t_start = idx[10]
    t_end = idx[10 + 120]  # 121 个点，约 120 分钟
    s.loc[t_start:t_end] = 1.5  # baseline + 1.0

    ev = EventWindow("E1", t_start, t_end, total_mm=10)
    v, peak = rdii(s, ev, baseline=0.5, recession_tail_h=0)
    # 期望约 1.0 m³/s × 120min × 60 = 7200 m³（容差 5%）
    assert v is not None
    assert v == pytest.approx(7200, rel=0.05)
    assert peak == pytest.approx(1.0, abs=1e-6)


def test_rdii_none_for_missing_baseline():
    s = _make_series([1.0] * 10)
    ev = EventWindow("E1", s.index[0], s.index[-1], total_mm=5)
    assert rdii(s, ev, baseline=None) == (None, None)


# ---------------------------------------------------------------------------
# 等效混接面积
# ---------------------------------------------------------------------------

def test_equivalent_illicit_area_formula():
    # V=10000 m³, P=20mm, C=0.8 → A = 10000 / (0.8 * 20 * 1000) = 0.625 km²
    a = equivalent_illicit_area(10000, rainfall_mm=20, runoff_coeff=0.8)
    assert a == pytest.approx(0.625, abs=1e-6)


def test_equivalent_illicit_area_invalid_inputs():
    assert equivalent_illicit_area(None, 20, 0.8) is None
    assert equivalent_illicit_area(10000, 0, 0.8) is None
    assert equivalent_illicit_area(10000, 20, 0) is None


# ---------------------------------------------------------------------------
# Qrl
# ---------------------------------------------------------------------------

def test_qrl_simple_sum_normalized_by_length():
    # Σ(V/R) = 10000/20 + 5000/10 = 500 + 500 = 1000
    # Σ(L) = 5 km
    # Qrl = 200 m³/(km·mm)
    out = qrl([10000, 5000], [20, 10], [5])
    assert out == pytest.approx(200, abs=1e-6)


# ---------------------------------------------------------------------------
# Rise amp / lags
# ---------------------------------------------------------------------------

def test_rise_amp_simple():
    s = _make_series([0.1, 0.2, 0.5, 1.0, 0.3, 0.2])
    ev = EventWindow("E1", s.index[0], s.index[-1], total_mm=5)
    r = rise_amp(s, ev, baseline_level=0.1, recession_tail_h=0)
    assert r == pytest.approx(0.9, abs=1e-6)


def test_lag_start_threshold_crossing():
    s = _make_series([0.10, 0.10, 0.20, 0.30, 0.50, 0.40])  # 阈值 0.05，3 个点后第一次跨过
    t0 = s.index[0]
    # s[1] = 0.10 not > 0.05 over baseline=0.10? baseline + threshold = 0.15
    # 跨越点是 idx[2] = 0.20，时间 20 min
    lag = lag_start(s, t0, baseline=0.10, rise_threshold=0.05, lag_max_hours=2)
    assert lag == pytest.approx(20 / 60, abs=1e-6)


def test_lag_peak_simple():
    s = _make_series([0.1, 0.2, 0.5, 1.0, 0.3])
    t0 = s.index[0]
    t_end = s.index[-1]
    lag = lag_peak(s, t0, t_end, recession_tail_h=0)
    # 峰值是 idx[3]，距 t0 = 30min
    assert lag == pytest.approx(30 / 60, abs=1e-6)


# ---------------------------------------------------------------------------
# Recession halflife
# ---------------------------------------------------------------------------

def test_recession_halflife_exponential_decay():
    # 真实半衰期 5 h，构造 y = baseline + 10 * exp(-t * ln2 / 5)
    n = 30
    t_h = np.arange(n) * 1.0
    baseline = 0.5
    y = baseline + 10 * np.exp(-t_h * np.log(2) / 5.0)
    idx = pd.date_range("2025-06-01", periods=n, freq="60min")
    s = pd.Series(y, index=idx)
    hl = recession_halflife(s, idx[0], baseline=baseline, fit_window_h=30)
    assert hl == pytest.approx(5.0, rel=0.05)


# ---------------------------------------------------------------------------
# Q-v-A consistency
# ---------------------------------------------------------------------------

def test_qv_a_consistency_within_tolerance():
    assert qv_a_consistency(flow_m3s=1.0, velocity_ms=0.5, cross_section_area_m2=2.0)
    assert not qv_a_consistency(flow_m3s=5.0, velocity_ms=0.5, cross_section_area_m2=2.0)
    # velocity 缺失时返回 True（无法判断）
    assert qv_a_consistency(flow_m3s=5.0, velocity_ms=None, cross_section_area_m2=2.0)
