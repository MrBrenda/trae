"""节点诊断：RDII 分级 + 问题类型判别。

诊断逻辑差异：
  污水节点（sewage）— 诊断重点
    · RDII 分级（rdii_grade）：High / Medium / Low / NA，基于液位中位升幅
    · 问题类型（category）：
        - 直连：时滞 ≤ 5 min + 升幅 ≥ 1 m（雨水直接接入）
        - 混接：升幅 High + 半衰期短/中（入流主导，管网混接）
        - 入渗：半衰期 ≥ 20 h + 升幅中低（地下水/渗漏入渗）
        - 未定：有响应但未达明确阈值
        - 数据不足：事件数 < 2 或可用率 < 30%

  雨水节点（stormwater）— 辅助诊断
    · 雨天应有较强响应（雨水管正常应汇水）
    · 响应弱（升幅 < 0.5 m）→ 雨水管低效（疑雨水进入污水系统）
    · 响应正常 → 运行良好

参考：《红旗东路积涝整治及管网改造专题研究阶段性成果报告 0423》表 5.4。
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd

from .io_paths import settings, sites

# RDII 等级定义（与 schema.py GRADE_VALUES 对齐）
RDII_GRADE_HIGH   = "High"
RDII_GRADE_MEDIUM = "Medium"
RDII_GRADE_LOW    = "Low"
RDII_GRADE_NA     = "NA"


# ---------------------------------------------------------------------------
# 单事件 RDII 分级
# ---------------------------------------------------------------------------

def grade_rdii(rise_amp_m: float | None) -> str:
    """依据单场事件液位升幅给出 High / Medium / Low / NA。"""
    if rise_amp_m is None or (isinstance(rise_amp_m, float) and np.isnan(rise_amp_m)):
        return RDII_GRADE_NA
    cfg = settings().get("diagnose", {})
    if rise_amp_m >= cfg.get("rise_amp_high_m", 3.0):
        return RDII_GRADE_HIGH
    if rise_amp_m <= cfg.get("rise_amp_low_m", 0.5):
        return RDII_GRADE_LOW
    return RDII_GRADE_MEDIUM


# ---------------------------------------------------------------------------
# 节点级综合诊断
# ---------------------------------------------------------------------------

def classify(
    node_id: str,
    stats: dict[str, Any],
    *,
    site_kind: str | None = None,
) -> tuple[str, str, float, str]:
    """综合判别 → (rdii_grade, category, evidence_score, notes)

    stats 字段：
        rise_amp_median   中位液位升幅 (m)
        lag_start_median  中位起始时滞 (h)
        halflife_median   中位回落半衰期 (h)
        n_events          有效事件数
        usable_rate       数据可用率
    """
    cfg        = settings().get("diagnose", {})
    high_rise  = cfg.get("rise_amp_high_m", 3.0)
    low_rise   = cfg.get("rise_amp_low_m", 0.5)
    direct_lag = cfg.get("direct_connection_lag_min", 5) / 60.0   # → 小时
    inf_hl     = cfg.get("infiltration_halflife_h", 20)
    inflow_hl  = cfg.get("inflow_halflife_h", 8)

    rise   = stats.get("rise_amp_median")
    lag    = stats.get("lag_start_median")
    hl     = stats.get("halflife_median")
    n_ev   = stats.get("n_events", 0)
    usable = stats.get("usable_rate", 0.0) or 0.0

    # 数据质量门槛
    if n_ev < 2 or usable < 0.3:
        return (RDII_GRADE_NA, "数据不足",
                min(usable, 0.5), f"有效事件 {n_ev} 场，可用率 {usable:.0%}，结论保留")

    rdii_grade = grade_rdii(rise)

    rise_s = f"{rise:.2f}" if rise is not None else "N/A"
    lag_s  = f"{lag*60:.0f}" if lag is not None else "N/A"
    hl_s   = f"{hl:.1f}" if hl is not None else "N/A"

    # ── 雨水节点 ──────────────────────────────────────────────────────────
    if site_kind == "stormwater":
        if rdii_grade == RDII_GRADE_LOW:
            return (rdii_grade, "雨水管低效", 0.8,
                    f"雨天升幅中位值 {rise_s} m，显著偏低，疑雨水汇入污水管网")
        return (rdii_grade, "未定", 0.5,
                f"雨天升幅 {rise_s} m，雨水管响应正常")

    # ── 污水节点 ──────────────────────────────────────────────────────────

    # 直连：时滞极短 + 有明显升幅
    if (lag is not None and lag <= direct_lag
            and rise is not None and rise >= 1.0):
        return (rdii_grade, "直连", 0.9,
                f"时滞 {lag_s} min（≤5 min）+ 升幅 {rise_s} m，疑雨水直连接入")

    # 入渗：半衰期长（缓慢消退）
    if hl is not None and hl >= inf_hl:
        notes = f"回落半衰期 {hl_s} h（≥{inf_hl} h），缓慢退水，地下水入渗主导"
        if rdii_grade == RDII_GRADE_HIGH:
            return (rdii_grade, "入渗", 0.75, notes)
        return (rdii_grade, "入渗", 0.80, notes)

    # 混接：高 RDII + 快速退水（入流主导）
    if rdii_grade == RDII_GRADE_HIGH:
        if hl is not None and hl <= inflow_hl:
            return (rdii_grade, "混接", 0.90,
                    f"升幅 {rise_s} m + 半衰期 {hl_s} h（≤{inflow_hl} h），雨水入流主导，疑管网混接")
        return (rdii_grade, "混接", 0.70,
                f"升幅 {rise_s} m，RDII 强烈，疑雨污混接")

    # 中度 RDII：有响应但未超阈值
    if rdii_grade == RDII_GRADE_MEDIUM:
        return (rdii_grade, "未定", 0.45,
                f"升幅 {rise_s} m，RDII 中等，需结合多场次数据进一步判断")

    # 低 RDII 污水节点：响应弱，暂无问题
    return (rdii_grade, "未定", 0.35,
            f"升幅 {rise_s} m，雨天响应弱，污水管网未见明显外来水入侵")


# ---------------------------------------------------------------------------
# 跨事件聚合 → node_diagnostics
# ---------------------------------------------------------------------------

def build_node_diagnostics(
    rdii_df: pd.DataFrame,
    usable_rate_by_node: dict[str, float] | None = None,
) -> pd.DataFrame:
    """从 rdii_by_event_node 聚合到 node_diagnostics（每节点一行）。"""
    usable_rate_by_node = usable_rate_by_node or {}
    site_cfg = (sites().get("nodes") or {})

    rows = []
    for nid, grp in rdii_df.groupby("node_id"):
        info  = site_cfg.get(nid, {})
        stats = {
            "rise_amp_median":  _safe_median(grp.get("rise_amp_m")),
            "lag_start_median": _safe_median(grp.get("lag_start_h")),
            "halflife_median":  _safe_median(grp.get("recession_halflife_h")),
            "n_events":         int(grp.shape[0]),
            "usable_rate":      usable_rate_by_node.get(nid, 1.0),
        }
        rdii_grade, cat, score, notes = classify(
            nid, stats, site_kind=info.get("kind")
        )
        rows.append({
            "node_id":              nid,
            "name_zh":              info.get("name_zh", nid),
            "pinyin":               info.get("pinyin", ""),
            "kind":                 info.get("kind", "sewage"),
            "n_events":             stats["n_events"],
            "rdii_grade":           rdii_grade,
            "mean_rise_amp_m":      _safe_mean(grp.get("rise_amp_m")),
            "median_lag_start_h":   stats["lag_start_median"],
            "median_halflife_h":    stats["halflife_median"],
            "mean_qrl":             _safe_mean(grp.get("qrl")),
            "mean_illicit_area_km2": _safe_mean(
                _pick(grp, ["illicit_area_km2_low", "illicit_area_km2"])
            ),
            "category":             cat,
            "evidence_score":       score,
            "notes":                notes,
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
