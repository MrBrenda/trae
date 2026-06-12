"""跨事件 × 跨节点的指标编排：填充 bwf_by_node 与 rdii_by_event_node。"""

from __future__ import annotations

import pandas as pd

from .io_paths import paths, settings, sites
from .metrics import (
    EventWindow,
    bwf,
    equivalent_illicit_area,
    lag_peak,
    lag_start,
    rdii,
    recession_halflife,
    rise_amp,
)
from .spatial import station_for_node


def _events_to_windows(df: pd.DataFrame) -> list[EventWindow]:
    """返回全部统一降雨事件的 EventWindow 列表（跨站合并后，全区共用同一张事件表）。"""
    return [
        EventWindow(
            event_id=row["event_id"],
            t_start=pd.Timestamp(row["t_start"]),
            t_end=pd.Timestamp(row["t_end"]),
            total_mm=float(row["total_mm"]),
        )
        for _, row in df.iterrows()
    ]


def _series_at_node(level_df: pd.DataFrame, node_id: str, value_col: str) -> pd.Series:
    sub = level_df[level_df["node_id"] == node_id].copy()
    if sub.empty:
        return pd.Series(dtype=float)
    # 只保留 good
    sub = sub[sub["qc_flag"] == "good"] if "qc_flag" in sub.columns else sub
    sub = sub.sort_values("ts")
    s = pd.Series(sub[value_col].to_numpy(), index=pd.DatetimeIndex(sub["ts"]))
    return s


def run_metrics() -> dict[str, pd.DataFrame]:
    """主入口：读 interim parquet → 跑指标 → 写 processed parquet。"""
    p = paths()
    cfg = settings()
    bwf_cfg = cfg.get("bwf", {})
    rdii_cfg = cfg.get("rdii", {})
    resp_cfg = cfg.get("response", {})
    illicit_cfg = cfg.get("illicit_area", {})

    events_p = p.parquet("events")
    if not events_p.exists():
        raise FileNotFoundError(f"找不到 {events_p}，请先运行 monitorda events")
    events_df = pd.read_parquet(events_p)
    all_events = _events_to_windows(events_df)
    if not all_events:
        return {"bwf": pd.DataFrame(), "rdii": pd.DataFrame()}

    level_p = p.parquet("node_level_10min")
    flow_p = p.parquet("node_flow_10min")
    level_df = pd.read_parquet(level_p) if level_p.exists() else pd.DataFrame()
    flow_df = pd.read_parquet(flow_p) if flow_p.exists() else pd.DataFrame()

    bwf_rows: list[dict] = []
    rdii_rows: list[dict] = []

    node_ids: list[str] = sorted((sites().get("nodes") or {}).keys())

    for nid in node_ids:
        events = all_events  # 统一事件，全区共用

        level_s = _series_at_node(level_df, nid, "level_m") if not level_df.empty else pd.Series(dtype=float)
        flow_s = _series_at_node(flow_df, nid, "flow_m3s") if not flow_df.empty else pd.Series(dtype=float)

        for ev in events:
            # BWF
            b_q, ws, we, n = bwf(
                flow_s if not flow_s.empty else level_s,
                ev,
                window_days=bwf_cfg.get("window_days", 14),
                exclude_radius_h=bwf_cfg.get("exclude_radius_h", 48),
                other_events=events,
                estimator=bwf_cfg.get("estimator", "median"),
                min_samples=bwf_cfg.get("min_samples", 144),
            ) if not flow_s.empty or not level_s.empty else (None, None, None, 0)
            b_level, _, _, _ = bwf(
                level_s,
                ev,
                window_days=bwf_cfg.get("window_days", 14),
                exclude_radius_h=bwf_cfg.get("exclude_radius_h", 48),
                other_events=events,
                estimator=bwf_cfg.get("estimator", "median"),
                min_samples=bwf_cfg.get("min_samples", 144),
            ) if not level_s.empty else (None, None, None, 0)

            bwf_rows.append({
                "node_id": nid,
                "event_id": ev.event_id,
                "bwf_q_m3s": b_q if not flow_s.empty else None,
                "bwf_level_m": b_level,
                "window_start": ws if ws is not None else ev.t_start,
                "window_end": we if we is not None else ev.t_end,
                "n_samples": int(n),
            })

            # RDII（基于流量；流量缺失时不算体积，只算液位指标）
            v_rdii, rdii_peak = (None, None)
            if not flow_s.empty and b_q is not None:
                v_rdii, rdii_peak = rdii(
                    flow_s, ev, b_q,
                    recession_tail_h=rdii_cfg.get("recession_tail_h", 48),
                )

            r_amp = rise_amp(
                level_s, ev, b_level,
                recession_tail_h=rdii_cfg.get("recession_tail_h", 48),
            ) if not level_s.empty else None

            l_start = lag_start(
                level_s if not level_s.empty else flow_s,
                ev.t_start, b_level if not level_s.empty else b_q,
                rise_threshold=resp_cfg.get("rise_threshold_m", 0.05),
                lag_max_hours=resp_cfg.get("lag_max_hours", 24),
            ) if (not level_s.empty or not flow_s.empty) else None

            l_peak = lag_peak(
                level_s if not level_s.empty else flow_s,
                ev.t_start, ev.t_end,
                recession_tail_h=rdii_cfg.get("recession_tail_h", 48),
            ) if (not level_s.empty or not flow_s.empty) else None

            hl = recession_halflife(
                level_s if not level_s.empty else flow_s,
                ev.t_end, b_level if not level_s.empty else b_q,
                fit_window_h=resp_cfg.get("recession_fit_window_h", 48),
            ) if (not level_s.empty or not flow_s.empty) else None

            area_low = equivalent_illicit_area(v_rdii, ev.total_mm, illicit_cfg.get("runoff_coeff_low", 0.78))
            area_high = equivalent_illicit_area(v_rdii, ev.total_mm, illicit_cfg.get("runoff_coeff_high", 0.90))

            from .diagnose import grade_rdii
            rdii_rows.append({
                "node_id": nid,
                "event_id": ev.event_id,
                "v_rdii_m3": v_rdii,
                "rdii_peak_m3s": rdii_peak,
                "rise_amp_m": r_amp,
                "lag_start_h": l_start,
                "lag_peak_h": l_peak,
                "recession_halflife_h": hl,
                "illicit_area_km2_low": area_low,
                "illicit_area_km2_high": area_high,
                "qrl": None,  # 单节点单事件不算 Qrl，留给跨节点聚合
                "grade": grade_rdii(r_amp),
            })

    bwf_df = pd.DataFrame(bwf_rows)
    rdii_df = pd.DataFrame(rdii_rows)

    if not bwf_df.empty:
        bwf_df.to_parquet(p.parquet("bwf_by_node"), index=False)
    if not rdii_df.empty:
        rdii_df.to_parquet(p.parquet("rdii_by_event_node"), index=False)

    return {"bwf": bwf_df, "rdii": rdii_df}
