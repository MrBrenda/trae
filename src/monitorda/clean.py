"""QC：行级 qc_flag 标记 + 节点级 null/stuck 报告。"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .io_paths import settings


# 标记取值约定
FLAG_GOOD = "good"
FLAG_NULL = "null"
FLAG_STUCK0 = "stuck0"
FLAG_IMPOSSIBLE = "impossible"
FLAG_OUTLIER = "outlier"


# ---------------------------------------------------------------------------
# 各表 QC
# ---------------------------------------------------------------------------

def qc_level(df: pd.DataFrame) -> pd.DataFrame:
    """液位：null → null，明显负值或 > 极端阈值 → impossible，连续 stuck_zero_window_h 为 0 → stuck0。"""
    cfg = settings().get("clean", {})
    stuck_h = cfg.get("stuck_zero_window_h", 6)

    df = df.copy()
    if "level_m" not in df.columns:
        return df
    flag = np.full(len(df), FLAG_GOOD, dtype=object)
    flag[df["level_m"].isna().to_numpy()] = FLAG_NULL
    flag[(df["level_m"] < 0).to_numpy()] = FLAG_IMPOSSIBLE
    flag[(df["level_m"] > 20).to_numpy()] = FLAG_IMPOSSIBLE  # 管道液位 > 20m 不现实

    # stuck zero 检测（按 node_id 分组）
    if "node_id" in df.columns:
        df["_flag_buf"] = flag
        for _, grp in df.groupby("node_id"):
            stuck_idx = _stuck_zero_indices(grp, "level_m", stuck_h)
            df.loc[stuck_idx, "_flag_buf"] = FLAG_STUCK0
        flag = df["_flag_buf"].to_numpy()
        df = df.drop(columns="_flag_buf")
    df["qc_flag"] = flag
    return df


def qc_flow(df: pd.DataFrame, sites_geom: dict | None = None) -> pd.DataFrame:
    """流量：null / 负值 / 物理不可能（> impossible_factor × 满管流量）/ stuck0。

    sites_geom: { node_id: { full_pipe_q_m3s: float, area_m2: float, ... } }
    """
    cfg = settings().get("clean", {})
    factor = cfg.get("flow_impossible_factor", 10.0)
    stuck_h = cfg.get("stuck_zero_window_h", 6)
    iqr_k = cfg.get("outlier_iqr_k", 5.0)

    df = df.copy()
    if "flow_m3s" not in df.columns:
        return df
    flag = np.full(len(df), FLAG_GOOD, dtype=object)
    flag[df["flow_m3s"].isna().to_numpy()] = FLAG_NULL
    flag[(df["flow_m3s"] < 0).to_numpy()] = FLAG_IMPOSSIBLE

    if sites_geom and "node_id" in df.columns:
        for nid, grp in df.groupby("node_id"):
            geom = sites_geom.get(nid, {})
            q_full = geom.get("full_pipe_q_m3s")
            if q_full and not math.isnan(q_full):
                limit = factor * q_full
                bad = (grp["flow_m3s"] > limit).to_numpy()
                flag[grp.index[bad]] = FLAG_IMPOSSIBLE

    # IQR 离群（按 node 分组）
    if "node_id" in df.columns:
        for nid, grp in df.groupby("node_id"):
            v = grp["flow_m3s"].dropna()
            if len(v) < 100:
                continue
            q1, q3 = v.quantile([0.25, 0.75])
            iqr = q3 - q1
            if iqr <= 0:
                continue
            hi = q3 + iqr_k * iqr
            lo = q1 - iqr_k * iqr
            mask = ((grp["flow_m3s"] > hi) | (grp["flow_m3s"] < lo)).to_numpy()
            # 不覆盖已经判为 impossible 的
            idx = grp.index[mask]
            still_good = flag[idx] == FLAG_GOOD
            flag[idx[still_good]] = FLAG_OUTLIER

    # stuck zero
    if "node_id" in df.columns:
        df["_flag_buf"] = flag
        for _, grp in df.groupby("node_id"):
            stuck_idx = _stuck_zero_indices(grp, "flow_m3s", stuck_h)
            df.loc[stuck_idx, "_flag_buf"] = FLAG_STUCK0
        flag = df["_flag_buf"].to_numpy()
        df = df.drop(columns="_flag_buf")
    df["qc_flag"] = flag
    return df


def _stuck_zero_indices(df: pd.DataFrame, value_col: str, window_h: float) -> pd.Index:
    """识别连续 value=0 且持续 >= window_h 小时的行。"""
    if "ts" not in df.columns or value_col not in df.columns:
        return pd.Index([])
    df = df.sort_values("ts")
    is_zero = (df[value_col] == 0).to_numpy()
    if not is_zero.any():
        return pd.Index([])
    ts = pd.to_datetime(df["ts"]).to_numpy()
    stuck_idx: list = []
    n = len(df)
    i = 0
    while i < n:
        if not is_zero[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and is_zero[j + 1]:
            j += 1
        span_h = (ts[j] - ts[i]).astype("timedelta64[s]").astype(float) / 3600.0
        if span_h >= window_h:
            stuck_idx.extend(df.index[i:j + 1].tolist())
        i = j + 1
    return pd.Index(stuck_idx)


# ---------------------------------------------------------------------------
# 节点级质量打分（对应原报告 表 2.2 + 4.2）
# ---------------------------------------------------------------------------

def null_rate_report(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """每个 node 的可用率统计 + qc_flag 分布。"""
    if "node_id" not in df.columns:
        return pd.DataFrame()
    out = []
    for nid, grp in df.groupby("node_id"):
        total = len(grp)
        null = int(grp["qc_flag"].eq(FLAG_NULL).sum())
        stuck0 = int(grp["qc_flag"].eq(FLAG_STUCK0).sum())
        imposs = int(grp["qc_flag"].eq(FLAG_IMPOSSIBLE).sum())
        outl = int(grp["qc_flag"].eq(FLAG_OUTLIER).sum())
        good = int(grp["qc_flag"].eq(FLAG_GOOD).sum())
        usable = good
        out.append({
            "node_id": nid,
            "total": total,
            "good": good,
            "null": null,
            "stuck0": stuck0,
            "impossible": imposs,
            "outlier": outl,
            "usable_rate": usable / total if total else None,
            "grade": _quality_grade(usable / total if total else 0),
        })
    return pd.DataFrame(out).sort_values("node_id").reset_index(drop=True)


def _quality_grade(rate: float) -> str:
    if rate >= 0.95:
        return "A"
    if rate >= 0.80:
        return "B"
    if rate >= 0.50:
        return "C"
    return "D"


# ---------------------------------------------------------------------------
# 顶层入口
# ---------------------------------------------------------------------------

def run_clean(*, sites_geom: dict | None = None) -> dict:
    """读取 interim parquet，跑 QC，再写回。返回每张表的可用率。"""
    from .io_paths import paths
    p = paths()
    out: dict[str, dict] = {}

    level_p = p.parquet("node_level_10min")
    if level_p.exists():
        df = pd.read_parquet(level_p)
        df = qc_level(df)
        df.to_parquet(level_p, index=False)
        out["node_level_10min"] = {
            "report": null_rate_report(df, "level_m").to_dict(orient="records"),
        }

    flow_p = p.parquet("node_flow_10min")
    if flow_p.exists():
        df = pd.read_parquet(flow_p)
        df = qc_flow(df, sites_geom=sites_geom)
        df.to_parquet(flow_p, index=False)
        out["node_flow_10min"] = {
            "report": null_rate_report(df, "flow_m3s").to_dict(orient="records"),
        }

    plant_p = p.parquet("plant_inlet_10min")
    if plant_p.exists():
        df = pd.read_parquet(plant_p)
        # 厂内入流暂时只标 null
        df["qc_flag"] = np.where(df["flow_m3s"].isna(), FLAG_NULL, FLAG_GOOD)
        df.to_parquet(plant_p, index=False)

    return out
