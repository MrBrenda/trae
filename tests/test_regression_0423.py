"""与 0423 docx 的回归对照测试。

仅在 data/raw/ 已就位且 processed parquet 存在时才执行；否则 skip。
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
import yaml

from monitorda.io_paths import paths, settings


pytestmark = pytest.mark.regression


def _expected() -> dict:
    p = Path(__file__).parent / "expected_0423.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def _has_raw_data() -> bool:
    p = paths()
    return any(p.raw.glob("*/*"))


@pytest.mark.skipif(not _has_raw_data(), reason="data/raw/ 为空，跳过 0423 回归")
def test_event_dates_match():
    """识别出的事件日期应覆盖 0423 报告 5 个事件。"""
    events_p = paths().parquet("events")
    if not events_p.exists():
        pytest.skip("尚未生成 events.parquet，先运行 monitorda events")
    ev = pd.read_parquet(events_p)
    expected_dates = {"2025-06-14", "2025-07-19", "2025-09-16", "2025-10-10", "2026-03-14"}
    actual_dates = set(ev["t_start"].dt.date.astype(str))
    missing = expected_dates - actual_dates
    assert not missing, f"未识别到事件：{missing}"


@pytest.mark.skipif(not _has_raw_data(), reason="data/raw/ 为空，跳过 0423 回归")
def test_diagnostics_category_match():
    """节点综合分类应与 0423 表 5.4 一致。"""
    diag_p = paths().parquet("node_diagnostics")
    if not diag_p.exists():
        pytest.skip("尚未生成 node_diagnostics.parquet，先运行 pipeline")
    diag = pd.read_parquet(diag_p)
    exp = _expected().get("diagnostics") or {}
    mismatches = []
    for nid, fields in exp.items():
        row = diag[diag["node_id"] == nid]
        if row.empty:
            mismatches.append(f"{nid}: missing")
            continue
        actual_cat = row.iloc[0]["category"]
        if actual_cat != fields["category"]:
            mismatches.append(f"{nid}: expected={fields['category']} actual={actual_cat}")
    assert not mismatches, "\n".join(mismatches)


@pytest.mark.skipif(not _has_raw_data(), reason="data/raw/ 为空，跳过 0423 回归")
def test_rdii_values_within_tolerance():
    rdii_p = paths().parquet("rdii_by_event_node")
    if not rdii_p.exists():
        pytest.skip("尚未生成 rdii_by_event_node.parquet，先运行 metrics")
    rdii = pd.read_parquet(rdii_p)
    cfg = settings().get("verify", {})
    tol_pct = cfg.get("rdii_tolerance_pct", 10) / 100.0

    exp = _expected().get("rdii") or {}
    failures = []
    for ev_id, nodes in exp.items():
        for nid, fields in (nodes or {}).items():
            actual = rdii[(rdii["event_id"] == ev_id) & (rdii["node_id"] == nid)]
            if actual.empty:
                failures.append(f"{ev_id}/{nid}: missing")
                continue
            r = actual.iloc[0]
            for f, exp_v in fields.items():
                if f not in r:
                    continue
                act_v = r[f]
                if pd.isna(act_v):
                    failures.append(f"{ev_id}/{nid}/{f}: NaN")
                    continue
                if exp_v == 0:
                    if abs(act_v) > tol_pct:
                        failures.append(f"{ev_id}/{nid}/{f}: exp=0 act={act_v}")
                else:
                    err = abs(act_v - exp_v) / abs(exp_v)
                    if err > tol_pct:
                        failures.append(f"{ev_id}/{nid}/{f}: exp={exp_v} act={act_v} err={err:.1%}")
    assert not failures, "\n".join(failures)
