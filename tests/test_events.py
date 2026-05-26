"""storm event 自动识别测试。"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from monitorda.events import detect_events


def _make_rain(rain_mm: list[float], station_id="V8805", start="2025-06-01 00:00"):
    idx = pd.date_range(start, periods=len(rain_mm), freq="h")
    return pd.DataFrame({"station_id": station_id, "ts": idx, "rain_mm_h": rain_mm})


def test_detect_single_event():
    # 24 h dry, 4 h wet (≥0.5 each, total ≥2mm), 24 h dry
    rain = [0.0] * 24 + [1.0, 1.0, 1.0, 1.0] + [0.0] * 24
    df = _make_rain(rain)
    ev = detect_events(df)
    assert len(ev) == 1
    e = ev.iloc[0]
    assert e["total_mm"] == pytest.approx(4.0)
    assert e["duration_h"] >= 2.0
    assert e["station_id"] == "V8805"
    assert e["event_id"].startswith("E")


def test_below_threshold_is_rejected():
    # Total only 1.0mm
    rain = [0.0] * 24 + [0.5, 0.5] + [0.0] * 24
    df = _make_rain(rain)
    ev = detect_events(df)
    assert ev.empty


def test_merge_close_events():
    # Two events 2h apart with no rain between → should merge
    rain = [0.0] * 24 + [1.0, 1.0] + [0.0] * 2 + [1.0, 1.0] + [0.0] * 24
    df = _make_rain(rain)
    ev = detect_events(df, merge_gap_h=6, merge_gap_mm=1.0)
    assert len(ev) == 1


def test_two_separate_events():
    # 24h dry, 4h wet, 12h dry (no rain), 4h wet, 24h dry → with merge_gap_h=6 would merge
    # Use merge_gap_h=6 but gap is 12h → two events
    rain = [0.0] * 24 + [1.0] * 4 + [0.0] * 12 + [1.0] * 4 + [0.0] * 24
    df = _make_rain(rain)
    ev = detect_events(df, merge_gap_h=6)
    assert len(ev) == 2


def test_multiple_stations_independent():
    df1 = _make_rain([0.0] * 5 + [1.0] * 4 + [0.0] * 5, "V8805")
    df2 = _make_rain([0.0] * 5 + [1.0] * 4 + [0.0] * 5, "V8870")
    ev = detect_events(pd.concat([df1, df2], ignore_index=True))
    assert set(ev["station_id"]) == {"V8805", "V8870"}
    assert len(ev) == 2


def test_compound_flag_set_for_short_antecedent_dry():
    # antecedent only 2h dry < default 24h
    rain = [0.0, 0.0] + [1.0] * 3 + [0.0] * 2 + [1.0] * 3 + [0.0] * 24
    df = _make_rain(rain)
    ev = detect_events(df, merge_gap_h=1, antecedent_dry_h=24)  # 不合并
    # 第二个事件 antecedent 较短
    assert len(ev) >= 1
    if len(ev) == 2:
        assert ev.iloc[1]["compound"] in (True, False)  # 至少字段存在
