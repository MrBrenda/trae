"""diagnose 模块测试。"""

from __future__ import annotations

import pandas as pd
import pytest

from monitorda.diagnose import build_node_diagnostics, classify, grade_rdii


def test_grade_rdii_thresholds():
    assert grade_rdii(3.5) == "High"
    assert grade_rdii(1.5) == "Medium"
    assert grade_rdii(0.3) == "Low"
    assert grade_rdii(None) == "NA"


def test_classify_direct_connection():
    """时滞 < 5min + 升幅 ≥ 1m → 直连"""
    stats = {"rise_amp_median": 2.0, "lag_start_median": 0.05, "halflife_median": 5.0,
             "n_events": 3, "usable_rate": 0.9}
    cat, score, _ = classify("W19", stats, site_kind="sewage")
    assert cat == "直连"
    assert score >= 0.8


def test_classify_infiltration():
    stats = {"rise_amp_median": 1.5, "lag_start_median": 4.0, "halflife_median": 25.0,
             "n_events": 3, "usable_rate": 0.8}
    cat, _, _ = classify("W17", stats, site_kind="sewage")
    assert cat == "入渗"


def test_classify_illicit_connection():
    stats = {"rise_amp_median": 3.5, "lag_start_median": 2.0, "halflife_median": 4.0,
             "n_events": 3, "usable_rate": 0.85}
    cat, _, _ = classify("W13", stats, site_kind="sewage")
    assert cat == "混接"


def test_classify_stormwater_inefficient():
    stats = {"rise_amp_median": 0.2, "lag_start_median": 1.0, "halflife_median": 3.0,
             "n_events": 4, "usable_rate": 0.9}
    cat, _, _ = classify("S07", stats, site_kind="stormwater")
    assert cat == "雨水管低效"


def test_classify_insufficient_data():
    stats = {"rise_amp_median": 3.0, "lag_start_median": 2.0, "halflife_median": 4.0,
             "n_events": 1, "usable_rate": 0.1}
    cat, _, _ = classify("W11", stats, site_kind="sewage")
    assert cat == "数据不足"


def test_build_node_diagnostics_from_rdii():
    rdii = pd.DataFrame([
        {"node_id": "W13", "event_id": "E1", "rise_amp_m": 3.5, "lag_start_h": 2.0,
         "recession_halflife_h": 5.0, "illicit_area_km2_low": 0.3, "qrl": 100, "grade": "High"},
        {"node_id": "W13", "event_id": "E2", "rise_amp_m": 4.0, "lag_start_h": 3.0,
         "recession_halflife_h": 6.0, "illicit_area_km2_low": 0.35, "qrl": 110, "grade": "High"},
        {"node_id": "W17", "event_id": "E1", "rise_amp_m": 1.5, "lag_start_h": 4.0,
         "recession_halflife_h": 25.0, "illicit_area_km2_low": 0.1, "qrl": 40, "grade": "Medium"},
        {"node_id": "W17", "event_id": "E2", "rise_amp_m": 1.4, "lag_start_h": 4.5,
         "recession_halflife_h": 27.0, "illicit_area_km2_low": 0.1, "qrl": 38, "grade": "Medium"},
    ])
    out = build_node_diagnostics(rdii, usable_rate_by_node={"W13": 0.9, "W17": 0.85})
    assert set(out["node_id"]) == {"W13", "W17"}
    w13 = out[out["node_id"] == "W13"].iloc[0]
    w17 = out[out["node_id"] == "W17"].iloc[0]
    assert w13["category"] == "混接"
    assert w17["category"] == "入渗"
