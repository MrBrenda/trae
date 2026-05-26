"""节点诊断：RDII 分级 + 雨污混接 / 入渗 / 直连 / 雨水管低效 4 类问题判别。

判别逻辑参考 0423 报告 表 5.4 + 5.4 描述的综合评定原则：
- 升幅大 + 时滞短 + 半衰期短  → 入流主导（直连嫌疑或近端混接）
- 升幅小 + 时滞长 + 半衰期长  → 入渗主导
- 雨水节点雨天响应弱           → 雨水管低效
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd

from .io_paths import settings, sites


# ---------------------------------------------------------------------------
# 单节点-单事件分级
# ---------------------------------------------------------------------------

def grade_rdii(rise_amp_m: float | None) -> str:
    """0423 表 4.4：依据 Event 2–4 的中位升幅给出 High/Medium/Low/NA。"""
    if rise_amp_m is None or np.isnan(rise_amp_m):
        return "NA"
    cfg = settings().get("diagnose", {})
    if rise_amp_m >= cfg.get("rise_amp_high_m", 3.0):
        return "High"
    if rise_amp_m <= cfg.get("rise_amp_low_m", 0.5):
        return "Low"
    return "Medium"


# ---------------------------------------------------------------------------
# 节点级综合分类
# ---------------------------------------------------------------------------

def classify(
    node_id: str,
    stats: dict[str, Any],
    *,
    site_kind: str | None = None,
) -> tuple[str, float, str]:
    """综合判别 → (category, evidence_score, notes)

    输入 stats 字段：
        rise_amp_median   median 升幅
        lag_start_median  median 起始时滞（小时）
        halflife_median   median 回落半衰期（小时）
        n_events          有效事件数
        usable_rate       数据可用率
    返回 (category, evidence_score, notes)
    """
    cfg = settings().get("diagnose", {})
    high_rise = cfg.get("rise_amp_high_m", 3.0)
    low_rise = cfg.get("rise_amp_low_m", 0.5)
    direct_lag = cfg.get("direct_connection_lag_min", 5) / 60.0  # 转小时
    inf_hl = cfg.get("infiltration_halflife_h", 20)
    inflow_hl = cfg.get("inflow_halflife_h", 8)

    rise = stats.get("rise_amp_median")
    lag = stats.get("lag_start_median")
    hl = stats.get("halflife_median")
    n_ev = stats.get("n_events", 0)
    usable = stats.get("usable_rate", 0.0) or 0.0

    if n_ev < 2 or usable < 0.3:
        return "数据不足", min(usable, 0.5), "事件数或可用率不足，结论保留"

    # 雨水节点：响应弱 → 雨水管低效
    if site_kind == "stormwater":
        if rise is not None and rise < low_rise:
            return "雨水管低效", 0.8, f"雨天升幅 {rise:.2f}m 显著偏低，疑雨水进入污水系统"
        return "未定", 0.4, "雨水节点响应正常，无明显问题"

    # 污水节点
    # 直连判定：时滞极短 + 升幅大
    if lag is not None and lag <= direct_lag and rise is not None and rise >= 1.0:
        return "直连", 0.9, f"时滞 {lag*60:.0f} 分钟 + 升幅 {rise:.2f}m，疑直连"

    # 入渗判定：半衰期长 + 升幅中低
    if hl is not None and hl >= inf_hl and rise is not None and rise < high_rise:
        return "入渗", 0.7, f"回落半衰期 {hl:.1f}h，缓慢退水，入渗主导"

    # 入流主导（混接）：升幅大 + 半衰期短/中
    if rise is not None and rise >= high_rise:
        if hl is not None and hl <= inflow_hl:
            return "混接", 0.85, f"升幅 {rise:.2f}m + 半衰期 {hl:.1f}h，入流主导"
        return "混接", 0.7, f"升幅 {rise:.2f}m，疑雨污混接"

    return "未定", 0.5, "综合特征未达任一明确阈值"


# ---------------------------------------------------------------------------
# 跨事件聚合
# ---------------------------------------------------------------------------

def build_node_diagnostics(
    rdii_df: pd.DataFrame,
    usable_rate_by_node: dict[str, float] | None = None,
) -> pd.DataFrame:
    """从 rdii_by_event_node 汇总到 node_diagnostics。"""
    usable_rate_by_node = usable_rate_by_node or {}
    site_cfg = (sites().get("nodes") or {})

    rows = []
    for nid, grp in rdii_df.groupby("node_id"):
        info = site_cfg.get(nid, {})
        stats = {
            "rise_amp_median": _safe_median(grp.get("rise_amp_m")),
            "lag_start_median": _safe_median(grp.get("lag_start_h")),
            "halflife_median": _safe_median(grp.get("recession_halflife_h")),
            "n_events": int(grp.shape[0]),
            "usable_rate": usable_rate_by_node.get(nid, 1.0),
        }
        cat, score, notes = classify(nid, stats, site_kind=info.get("kind"))

        rows.append({
            "node_id": nid,
            "name_zh": info.get("name_zh", nid),
            "kind": info.get("kind", "sewage"),
            "n_events": stats["n_events"],
            "mean_qrl": _safe_mean(grp.get("qrl")),
            "mean_illicit_area_km2": _safe_mean(
                _pick(grp, ["illicit_area_km2_low", "illicit_area_km2"])
            ),
            "mean_rise_amp_m": _safe_mean(grp.get("rise_amp_m")),
            "median_lag_start_h": stats["lag_start_median"],
            "median_halflife_h": stats["halflife_median"],
            "category": cat,
            "evidence_score": score,
            "notes": notes,
        })

    return pd.DataFrame(rows).sort_values("node_id").reset_index(drop=True)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _safe_median(s) -> float | None:
    if s is None:
        return None
    arr = pd.Series(s).dropna()
    return float(arr.median()) if not arr.empty else None


def _safe_mean(s) -> float | None:
    if s is None:
        return None
    arr = pd.Series(s).dropna()
    return float(arr.mean()) if not arr.empty else None


def _pick(grp: pd.DataFrame, candidates: Iterable[str]):
    for c in candidates:
        if c in grp.columns:
            return grp[c]
    return None
