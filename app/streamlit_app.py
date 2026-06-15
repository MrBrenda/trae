"""排水管网在线监测数据自动化诊断 — Streamlit 看板

运行方式：
    make app
    # 或
    .venv/bin/streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── 路径初始化 ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import yaml  # noqa: E402
from monitorda.io_paths import paths  # noqa: E402

# ── 常量 ──────────────────────────────────────────────────────────────────────
CATEGORY_COLORS: dict[str, str] = {
    "混接":     "#d62728",
    "入渗":     "#ff7f0e",
    "直连":     "#8b0000",
    "雨水管低效": "#1f77b4",
    "未定":     "#7f7f7f",
    "数据不足":  "#cccccc",
}

PIPELINE_STAGES = [
    ("ingest",   "① 数据导入"),
    ("clean",    "② 质量控制"),
    ("events",   "③ 事件识别"),
    ("metrics",  "④ 指标计算"),
    ("diagnose", "⑤ 节点诊断"),
    ("report",   "⑥ 生成报告"),
]

PARQUET_STATUS_ITEMS = [
    ("node_level_10min",   "液位数据"),
    ("node_flow_10min",    "流量数据"),
    ("rainfall_hourly",    "雨量数据"),
    ("events",             "降雨事件"),
    ("bwf_by_node",        "BWF 基线"),
    ("rdii_by_event_node", "RDII 指标"),
    ("node_diagnostics",   "节点诊断"),
]

# ── 数据加载（带缓存）────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def load_parquet(kind: str) -> pd.DataFrame:
    p = paths().parquet(kind)
    if not p.exists():
        return pd.DataFrame()
    return pd.read_parquet(p)


@st.cache_data(ttl=30)
def get_site_cfg() -> dict:
    # 直接读文件，避免 io_paths.sites() 的 lru_cache 导致 sites.yaml 更新后不刷新
    with paths().cfg_sites.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── 辅助函数 ──────────────────────────────────────────────────────────────────

def parquet_exists(kind: str) -> bool:
    return paths().parquet(kind).exists()


def node_label(node_id: str, cfg: dict) -> str:
    info = (cfg.get("nodes") or {}).get(node_id, {})
    pinyin = info.get("pinyin", "")
    name   = info.get("name_zh", node_id)
    # 优先显示拼音缩写（保密场景），无拼音时回退到中文简称
    label  = pinyin if pinyin else name
    return f"{node_id}  {label}"


def run_stage(cmd: str) -> subprocess.CompletedProcess:
    mon_bin = ROOT / ".venv" / "bin" / "monitorda"
    return subprocess.run(
        [str(mon_bin), cmd],
        capture_output=True, text=True, cwd=str(ROOT),
    )


# ── 页面配置 ──────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="排水管网诊断看板",
    page_icon="🌧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("排水管网在线监测数据自动化诊断")
st.caption("红旗东路积涝整治示范区 · 第五污水厂服务范围（26 监测节点）")

# ── 侧边栏 ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("📁 数据状态")
    for kind, label in PARQUET_STATUS_ITEMS:
        icon = "✅" if parquet_exists(kind) else "⬜"
        st.write(f"{icon} {label}")

    st.divider()
    st.header("🔎 节点筛选")

    site_cfg = get_site_cfg()
    all_nodes = list((site_cfg.get("nodes") or {}).keys())

    kind_filter = st.radio("节点类型", ["全部", "雨水 (S)", "污水 (W)"], horizontal=True)
    if kind_filter == "雨水 (S)":
        available_nodes = [n for n in all_nodes if n.startswith("S")]
    elif kind_filter == "污水 (W)":
        available_nodes = [n for n in all_nodes if n.startswith("W")]
    else:
        available_nodes = all_nodes

    selected_node = st.selectbox(
        "当前节点",
        available_nodes,
        format_func=lambda n: node_label(n, site_cfg),
    )

    st.divider()
    if st.button("🔄 刷新缓存", width="stretch"):
        st.cache_data.clear()
        st.rerun()

# ── 主区域：标签页 ────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 数据总览",
    "🌧 降雨事件",
    "📈 指标分析",
    "🔍 诊断结果",
    "⚙️ 流水线",
])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1  数据总览
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    level_df = load_parquet("node_level_10min")
    flow_df  = load_parquet("node_flow_10min")
    rain_df  = load_parquet("rainfall_hourly")

    if level_df.empty and flow_df.empty:
        st.info("暂无 interim 数据，请前往「⚙️ 流水线」Tab 运行「① 数据导入」。")
    else:
        # ── 节点信息 ──────────────────────────────────────────────────────────
        node_info = (site_cfg.get("nodes") or {}).get(selected_node, {})
        info_col, chart_col = st.columns([1, 4])

        with info_col:
            st.subheader(node_label(selected_node, site_cfg))
            st.markdown(f"- **类型**：{'雨水' if selected_node.startswith('S') else '污水'}节点")
            road = node_info.get("road", "")
            if road:
                st.markdown(f"- **位置**：{road}")
            note = node_info.get("note", "")
            if note:
                st.markdown(f"- **备注**：{note}")

        with chart_col:
            nd_lvl = (level_df[level_df["node_id"] == selected_node].copy()
                      if not level_df.empty else pd.DataFrame())

            if nd_lvl.empty:
                st.warning(f"节点 {selected_node} 暂无液位时序数据。")
            else:
                # 液位 + 雨量双轴图
                fig_ts = go.Figure()
                good = nd_lvl["qc_flag"] == "good"
                fig_ts.add_trace(go.Scatter(
                    x=nd_lvl.loc[good, "ts"], y=nd_lvl.loc[good, "level_m"],
                    mode="lines", line=dict(width=1.2, color="#2ca02c"),
                    name="液位 (good)",
                ))
                bad_pts = nd_lvl[~good]
                if not bad_pts.empty:
                    fig_ts.add_trace(go.Scatter(
                        x=bad_pts["ts"], y=bad_pts["level_m"],
                        mode="markers", marker=dict(size=3, color="#d62728"),
                        name="液位 (异常)",
                    ))
                if not rain_df.empty and "ts" in rain_df.columns:
                    fig_ts.add_trace(go.Bar(
                        x=rain_df["ts"], y=rain_df["rain_mm_h"],
                        marker_color="rgba(30,144,255,0.20)",
                        name="降雨强度 mm/h", yaxis="y2",
                    ))
                fig_ts.update_layout(
                    xaxis_title="时间",
                    yaxis=dict(title="液位 m"),
                    yaxis2=dict(title="降雨强度 mm/h", overlaying="y", side="right",
                                showgrid=False, rangemode="tozero"),
                    legend=dict(orientation="h", y=-0.25),
                    height=320, margin=dict(t=30, b=10),
                )
                st.plotly_chart(fig_ts, width="stretch")

        # ── 流量图（次要） ──────────────────────────────────────────────────
        if not flow_df.empty:
            nd_flw = flow_df[flow_df["node_id"] == selected_node].copy()
            if not nd_flw.empty:
                good_q = nd_flw["qc_flag"] == "good"
                fig_q = go.Figure()
                fig_q.add_trace(go.Scatter(
                    x=nd_flw.loc[good_q, "ts"], y=nd_flw.loc[good_q, "flow_m3s"],
                    mode="lines", line=dict(width=1, color="#1f77b4"), name="流量 m³/s",
                ))
                fig_q.update_layout(
                    xaxis_title="时间", yaxis_title="流量 m³/s",
                    height=240, margin=dict(t=20, b=10),
                )
                st.plotly_chart(fig_q, width="stretch")

        # ── QC 分布（全节点汇总） ───────────────────────────────────────────
        st.subheader("全节点 QC 标志分布")
        qc_col_l, qc_col_r = st.columns(2)
        qc_color_map = {
            "good": "#2ca02c", "null": "#aaaaaa", "stuck0": "#ff7f0e",
            "impossible": "#d62728", "outlier": "#9467bd", "communication_loss": "#8c564b",
        }
        for col, df, lbl in [(qc_col_l, level_df, "液位"), (qc_col_r, flow_df, "流量")]:
            with col:
                if df.empty or "qc_flag" not in df.columns:
                    st.info(f"暂无{lbl}数据")
                else:
                    counts = df["qc_flag"].value_counts().reset_index()
                    counts.columns = ["qc_flag", "count"]
                    fig_qc = px.pie(
                        counts, names="qc_flag", values="count",
                        title=f"{lbl} QC 分布",
                        color="qc_flag", color_discrete_map=qc_color_map,
                    )
                    fig_qc.update_layout(height=280, margin=dict(t=40, b=10))
                    st.plotly_chart(fig_qc, width="stretch")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2  降雨事件
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    events_df = load_parquet("events")

    if events_df.empty:
        st.info("暂无事件数据，请先运行「③ 事件识别」。")
    else:
        st.subheader(f"共识别降雨事件 {len(events_df)} 场")

        # KPI 卡片
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("事件总数",       f"{len(events_df)} 场")
        k2.metric("最大单场雨量",   f"{events_df['total_mm'].max():.1f} mm")
        k3.metric("最长持续时长",   f"{events_df['duration_h'].max():.1f} h")
        k4.metric("最大峰值雨强",   f"{events_df['max_intensity_mmh'].max():.1f} mm/h")
        n_st_col = "n_stations" if "n_stations" in events_df.columns else None
        k5.metric("最多覆盖雨量站",
                  f"{int(events_df[n_st_col].max())} 站" if n_st_col else "—")

        # 甘特时间轴
        _max_mm = events_df["total_mm"].max() or 1.0
        fig_gantt = go.Figure()
        for _, ev in events_df.iterrows():
            alpha = max(0.2, min(0.9, ev["total_mm"] / _max_mm))
            fig_gantt.add_trace(go.Scatter(
                x=[ev["t_start"], ev["t_end"]],
                y=[ev["event_id"], ev["event_id"]],
                mode="lines",
                line=dict(width=10, color=f"rgba(30,144,255,{alpha:.2f})"),
                showlegend=False,
                hovertemplate=(
                    f"<b>{ev['event_id']}</b><br>"
                    f"开始：{ev['t_start'].strftime('%Y-%m-%d %H:%M')}<br>"
                    f"结束：{ev['t_end'].strftime('%Y-%m-%d %H:%M')}<br>"
                    f"历时：{ev['duration_h']:.1f} h<br>"
                    f"雨量：{ev['total_mm']:.1f} mm  峰值雨强：{ev['max_intensity_mmh']:.1f} mm/h<br>"
                    + (f"覆盖雨量站：{int(ev['n_stations'])} 站" if "n_stations" in ev.index else "")
                    + "<extra></extra>"
                ),
            ))
        fig_gantt.update_layout(
            title="事件时间轴（颜色深浅 ∝ 累计雨量）",
            xaxis_title="时间", yaxis_title="事件 ID",
            height=max(220, len(events_df) * 42 + 80),
            margin=dict(t=40, b=40),
        )
        st.plotly_chart(fig_gantt, width="stretch")

        # 明细表
        st.subheader("事件明细表")
        _ev_cols_map = {
            "event_id": "事件ID", "station_id": "代表雨量站", "n_stations": "覆盖站数",
            "t_start": "开始时间", "t_end": "结束时间", "duration_h": "历时(h)",
            "total_mm": "累计雨量(mm)", "max_intensity_mmh": "峰值雨强(mm/h)",
            "antecedent_dry_d": "前期干旱天数", "compound": "复合事件",
        }
        _ev_present = [c for c in _ev_cols_map if c in events_df.columns]
        disp_ev = events_df[_ev_present].rename(columns=_ev_cols_map)
        st.dataframe(disp_ev, width="stretch", hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3  指标分析
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    rdii_df  = load_parquet("rdii_by_event_node")
    bwf_df   = load_parquet("bwf_by_node")
    level_df = load_parquet("node_level_10min")
    ev_df    = load_parquet("events")

    if rdii_df.empty:
        st.info("暂无 RDII 指标，请先运行「④ 指标计算」。")
    else:
        st.subheader("雨天响应指标总览")

        # 热力图：节点 × 事件 × 升幅
        pivot = (rdii_df.dropna(subset=["rise_amp_m"])
                 .pivot_table(index="node_id", columns="event_id",
                              values="rise_amp_m", aggfunc="mean"))
        if not pivot.empty:
            fig_heat = px.imshow(
                pivot,
                color_continuous_scale="Reds",
                aspect="auto",
                labels=dict(x="降雨事件", y="节点", color="升幅 m"),
                title="液位升幅热力图（节点 × 事件；颜色越深 = 雨天响应越强）",
            )
            fig_heat.update_layout(height=420, margin=dict(t=50, b=40))
            st.plotly_chart(fig_heat, width="stretch")

        col_sc, col_box = st.columns(2)

        # 散点：时滞 vs 升幅
        with col_sc:
            sc_df = rdii_df.dropna(subset=["lag_start_h", "rise_amp_m"])
            if not sc_df.empty:
                fig_sc = px.scatter(
                    sc_df, x="lag_start_h", y="rise_amp_m",
                    color="node_id", symbol="grade",
                    hover_data=["event_id", "recession_halflife_h"],
                    labels={"lag_start_h": "起始时滞 h", "rise_amp_m": "液位升幅 m"},
                    title="时滞 vs 升幅（诊断判别空间）",
                )
                fig_sc.add_hline(y=3.0, line_dash="dash", line_color="gray",
                                 annotation_text="升幅 High 阈值 3m")
                fig_sc.add_vline(x=5 / 60, line_dash="dash", line_color="red",
                                 annotation_text="直连阈值 5min")
                fig_sc.update_layout(height=380, margin=dict(t=40))
                st.plotly_chart(fig_sc, width="stretch")

        # 箱线图：回落半衰期
        with col_box:
            hl_df = rdii_df.dropna(subset=["recession_halflife_h"])
            if not hl_df.empty:
                fig_box = px.box(
                    hl_df, x="node_id", y="recession_halflife_h",
                    color="node_id",
                    labels={"recession_halflife_h": "回落半衰期 h", "node_id": "节点"},
                    title="各节点回落半衰期（入渗识别依据）",
                )
                fig_box.add_hline(y=20, line_dash="dot", line_color="orange",
                                  annotation_text="入渗阈值 20h")
                fig_box.update_layout(height=380, showlegend=False, margin=dict(t=40))
                st.plotly_chart(fig_box, width="stretch")

        # 单节点波形对比（选事件）
        st.subheader(f"节点波形对比 — {node_label(selected_node, site_cfg)}")
        all_event_ids = sorted(rdii_df["event_id"].unique().tolist())
        sel_events = st.multiselect(
            "选择事件（最多 4 场叠加显示）",
            all_event_ids,
            default=all_event_ids[:min(3, len(all_event_ids))],
            max_selections=4,
        )

        nd_lvl = (level_df[level_df["node_id"] == selected_node]
                  if not level_df.empty else pd.DataFrame())

        if sel_events and not nd_lvl.empty and not ev_df.empty:
            fig_wave = go.Figure()
            colors = px.colors.qualitative.Set2

            for i, eid in enumerate(sel_events):
                ev_row = ev_df[ev_df["event_id"] == eid]
                if ev_row.empty:
                    continue
                ev = ev_row.iloc[0]
                window = nd_lvl[
                    (nd_lvl["ts"] >= ev["t_start"] - pd.Timedelta(hours=6)) &
                    (nd_lvl["ts"] <= ev["t_end"]   + pd.Timedelta(hours=48))
                ]
                if window.empty:
                    continue

                fig_wave.add_trace(go.Scatter(
                    x=window["ts"], y=window["level_m"],
                    mode="lines", name=eid,
                    line=dict(width=1.5, color=colors[i % len(colors)]),
                ))

                # BWF 基线水平线
                if not bwf_df.empty:
                    bwf_row = bwf_df[
                        (bwf_df["node_id"] == selected_node) & (bwf_df["event_id"] == eid)
                    ]
                    if not bwf_row.empty:
                        bl = bwf_row["bwf_level_m"].iloc[0]
                        if pd.notna(bl):
                            fig_wave.add_hline(
                                y=bl, line_dash="dot", line_color=colors[i % len(colors)],
                                annotation_text=f"BWF {eid[:11]} ({bl:.2f}m)",
                                annotation_position="right",
                            )

            fig_wave.update_layout(
                title=f"{selected_node} 事件窗口液位波形（含 BWF 旱天基线）",
                xaxis_title="时间", yaxis_title="液位 m",
                height=360, margin=dict(t=40),
            )
            st.plotly_chart(fig_wave, width="stretch")
        elif sel_events and nd_lvl.empty:
            st.warning("该节点暂无液位时序数据。")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4  诊断结果
# ═══════════════════════════════════════════════════════════════════════════════

RDII_GRADE_COLORS = {
    "High":   "#d62728",
    "Medium": "#ff7f0e",
    "Low":    "#2ca02c",
    "NA":     "#cccccc",
}

with tab4:
    diag_df  = load_parquet("node_diagnostics")
    rdii_df2 = load_parquet("rdii_by_event_node")

    if diag_df.empty:
        st.info("暂无诊断结果，请先完成全部流水线步骤（至少运行到⑤）。")
    else:
        # ── 污水 / 雨水分开展示 ───────────────────────────────────────────────
        sewage_df    = diag_df[diag_df["kind"] == "sewage"].copy()
        stormwater_df = diag_df[diag_df["kind"] == "stormwater"].copy()

        # ── 顶部统计卡片 ──────────────────────────────────────────────────────
        st.subheader("污水节点 — RDII 诊断（诊断重点）")

        grade_counts = sewage_df["rdii_grade"].value_counts() if not sewage_df.empty else pd.Series(dtype=int)
        g_cols = st.columns(4)
        for gi, grade in enumerate(["High", "Medium", "Low", "NA"]):
            cnt = int(grade_counts.get(grade, 0))
            color = RDII_GRADE_COLORS[grade]
            g_cols[gi].markdown(
                f"<div style='background:{color}22;border-left:4px solid {color};"
                f"padding:8px 12px;border-radius:4px'>"
                f"<span style='color:{color};font-weight:700'>RDII {grade}</span><br>"
                f"<span style='font-size:1.6em;font-weight:700'>{cnt}</span>"
                f"<span style='font-size:0.85em'> 个节点</span></div>",
                unsafe_allow_html=True,
            )

        st.markdown("")
        sl, sr = st.columns([3, 2])

        with sl:
            # 污水节点明细表（RDII 为核心列）
            sew_cols = {
                "node_id": "节点ID", "pinyin": "拼音缩写",
                "n_events": "事件数", "rdii_grade": "RDII分级",
                "mean_rise_amp_m": "均值升幅(m)",
                "median_lag_start_h": "中位时滞(h)",
                "median_halflife_h": "中位半衰期(h)",
                "category": "问题类型", "evidence_score": "置信分", "notes": "备注",
            }
            present_s = [c for c in sew_cols if c in sewage_df.columns]
            disp_s = sewage_df[present_s].rename(columns=sew_cols)

            def _style_sewage(row: pd.Series) -> list[str]:
                styles = []
                for c in row.index:
                    if c == "RDII分级":
                        color = RDII_GRADE_COLORS.get(row[c], "#7f7f7f")
                        styles.append(f"background-color:{color}33;font-weight:700")
                    elif c == "问题类型":
                        color = CATEGORY_COLORS.get(row[c], "#7f7f7f")
                        styles.append(f"background-color:{color}22")
                    else:
                        styles.append("")
                return styles

            st.dataframe(
                disp_s.style.apply(_style_sewage, axis=1),
                width="stretch", hide_index=True, height=380,
            )

        with sr:
            # RDII 升幅条形图（仅污水节点）
            if not rdii_df2.empty and "rise_amp_m" in rdii_df2.columns:
                sew_ids = sewage_df["node_id"].tolist() if not sewage_df.empty else []
                agg_s = (rdii_df2[rdii_df2["node_id"].isin(sew_ids)]
                         .dropna(subset=["rise_amp_m"])
                         .groupby("node_id")["rise_amp_m"].median()
                         .reset_index()
                         .rename(columns={"rise_amp_m": "中位升幅"}))
                if not agg_s.empty:
                    agg_s = agg_s.merge(sewage_df[["node_id", "rdii_grade"]], on="node_id", how="left")
                    agg_s["color"] = agg_s["rdii_grade"].map(RDII_GRADE_COLORS).fillna("#cccccc")
                    agg_s = agg_s.sort_values("中位升幅")
                    fig_bar_s = go.Figure(go.Bar(
                        y=agg_s["node_id"], x=agg_s["中位升幅"],
                        orientation="h", marker_color=agg_s["color"],
                        hovertemplate="%{y}: %{x:.2f} m<extra></extra>",
                    ))
                    fig_bar_s.add_vline(x=3.0, line_dash="dash", line_color="gray",
                                        annotation_text="High 3m")
                    fig_bar_s.add_vline(x=0.5, line_dash="dot", line_color="gray",
                                        annotation_text="Low 0.5m")
                    fig_bar_s.update_layout(
                        title="污水节点中位升幅（颜色 = RDII 分级）",
                        xaxis_title="液位中位升幅 m", height=360, margin=dict(t=40),
                    )
                    st.plotly_chart(fig_bar_s, width="stretch")

            # 问题类型饼图（污水）
            if not sewage_df.empty:
                pie_s = sewage_df["category"].value_counts().reset_index()
                pie_s.columns = ["category", "count"]
                fig_pie_s = px.pie(
                    pie_s, names="category", values="count",
                    color="category", color_discrete_map=CATEGORY_COLORS,
                    title="污水节点问题类型分布",
                )
                fig_pie_s.update_layout(height=240, margin=dict(t=40, b=10))
                st.plotly_chart(fig_pie_s, width="stretch")

        # ── RTK 单位线分析 ────────────────────────────────────────────────────
        st.divider()
        st.subheader("RTK 单位线分析 — 快速入流 vs 慢速入渗定量分解")

        rtk_df = load_parquet("rtk_by_node")
        rtk_sew = (rtk_df[rtk_df["node_id"].str.startswith("W")].copy()
                   if not rtk_df.empty else pd.DataFrame())

        RTK_CAT_COLORS = {
            "fast_inflow":      "#d62728",
            "mixed":            "#ff7f0e",
            "slow_infiltration": "#1f77b4",
            "fit_unreliable":   "#aaaaaa",
            "data_insufficient": "#dddddd",
        }
        RTK_CAT_LABELS = {
            "fast_inflow":       "入流主导",
            "mixed":             "混合型",
            "slow_infiltration": "入渗主导",
            "fit_unreliable":    "拟合不可靠",
            "data_insufficient": "数据不足",
        }

        if rtk_sew.empty:
            st.info("暂无 RTK 分析结果，请先运行 `monitorda rtk`。")
        else:
            # 合并原诊断标签
            rtk_merged = rtk_sew.merge(
                sewage_df[["node_id", "pinyin", "category", "rdii_grade"]],
                on="node_id", how="left",
            )
            rtk_merged["rtk_label"] = rtk_merged["category_rtk"].map(RTK_CAT_LABELS)
            rtk_merged["slow_fraction"] = 1.0 - rtk_merged["fast_fraction"].fillna(0)

            rc1, rc2 = st.columns([3, 2])

            with rc1:
                # 堆叠条形图：快速入流 vs 慢速入渗比例
                fit_ok = rtk_merged[
                    ~rtk_merged["category_rtk"].isin(["data_insufficient", "fit_unreliable"])
                ].sort_values("fast_fraction", ascending=False)

                if fit_ok.empty:
                    st.info("可用 RTK 拟合结果不足，需要更多数据覆盖。")
                else:
                    labels = fit_ok["pinyin"].fillna(fit_ok["node_id"])
                    fig_rtk = go.Figure()
                    fig_rtk.add_trace(go.Bar(
                        name="快速入流 (R1)",
                        x=labels, y=fit_ok["fast_fraction"] * 100,
                        marker_color="#d62728", text=(fit_ok["fast_fraction"] * 100).round(0).astype(int).astype(str) + "%",
                        textposition="inside",
                    ))
                    fig_rtk.add_trace(go.Bar(
                        name="慢速入渗 (R2)",
                        x=labels, y=fit_ok["slow_fraction"] * 100,
                        marker_color="#1f77b4",
                    ))
                    fig_rtk.update_layout(
                        barmode="stack", height=300, margin=dict(t=40, b=10),
                        title="快速入流 / 慢速入渗分解比例（RTK 拟合）",
                        yaxis_title="%", legend=dict(orientation="h", y=1.12),
                    )
                    st.plotly_chart(fig_rtk, width="stretch")

            with rc2:
                # RTK 参数明细表
                rtk_cols = {
                    "node_id": "节点", "category": "规则诊断",
                    "category_rtk": "RTK分类",
                    "fast_fraction": "入流比例",
                    "T1_h": "T1(h)", "T2_h": "T2(h)",
                    "r2": "R²", "n_events_used": "事件数",
                }
                present_r = [c for c in rtk_cols if c in rtk_merged.columns]
                disp_r = rtk_merged[present_r].rename(columns=rtk_cols).copy()
                for col in ["入流比例", "R²"]:
                    if col in disp_r.columns:
                        disp_r[col] = disp_r[col].apply(
                            lambda v: f"{v:.0%}" if pd.notna(v) else "—"
                        )
                for col in ["T1(h)", "T2(h)"]:
                    if col in disp_r.columns:
                        disp_r[col] = disp_r[col].apply(
                            lambda v: f"{v:.1f}" if pd.notna(v) else "—"
                        )
                disp_r["RTK分类"] = disp_r["RTK分类"].map(RTK_CAT_LABELS).fillna(disp_r["RTK分类"])

                def _style_rtk(row):
                    styles = []
                    for c in row.index:
                        if c == "RTK分类":
                            inv_map = {v: k for k, v in RTK_CAT_LABELS.items()}
                            key = inv_map.get(row[c], row[c])
                            color = RTK_CAT_COLORS.get(key, "#7f7f7f")
                            styles.append(f"background-color:{color}22;font-weight:600")
                        else:
                            styles.append("")
                    return styles

                st.dataframe(
                    disp_r.style.apply(_style_rtk, axis=1),
                    width="stretch", hide_index=True, height=360,
                )

            # RTK 方法说明
            with st.expander("方法说明：RTK 三参数单位线"):
                st.markdown(
                    "**RTK 方法**（来源：EPA RDII Analysis / SSOAP Toolbox）使用两组三角形单位线，"
                    "分别拟合**快速入流**（雨水直连/混接，T1 = 峰值时间 < 12h）"
                    "和**慢速入渗**（地下水/管壁渗漏，T2 ≥ 24h）的贡献比例。\n\n"
                    "- **R1 / R2**：各分量对降雨量的响应系数（m 液位升幅 / mm 降雨），越大表示贡献越强\n"
                    "- **入流比例** = R1 / (R1 + R2)：超过 65% 为入流主导，低于 30% 为入渗主导\n"
                    "- **R²**：拟合优度（决定系数）。低于 0.05 标记为「拟合不可靠」，通常源于数据覆盖不足"
                )

        # ── 雨水节点 ──────────────────────────────────────────────────────────
        st.divider()
        st.subheader("雨水节点 — 运行状态")

        if stormwater_df.empty:
            st.info("暂无雨水节点诊断数据。")
        else:
            sw_cols = {
                "node_id": "节点ID", "pinyin": "拼音缩写",
                "n_events": "事件数", "rdii_grade": "响应强度",
                "mean_rise_amp_m": "均值升幅(m)",
                "category": "运行状态", "evidence_score": "置信分", "notes": "备注",
            }
            present_sw = [c for c in sw_cols if c in stormwater_df.columns]
            disp_sw = stormwater_df[present_sw].rename(columns=sw_cols)

            def _style_stormwater(row: pd.Series) -> list[str]:
                styles = []
                for c in row.index:
                    if c == "运行状态":
                        color = CATEGORY_COLORS.get(row[c], "#7f7f7f")
                        styles.append(f"background-color:{color}22")
                    elif c == "响应强度":
                        color = RDII_GRADE_COLORS.get(row[c], "#7f7f7f")
                        styles.append(f"background-color:{color}22")
                    else:
                        styles.append("")
                return styles

            st.dataframe(
                disp_sw.style.apply(_style_stormwater, axis=1),
                width="stretch", hide_index=True,
            )

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 5  流水线
# ═══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.subheader("流水线控制")
    st.caption("各阶段需按顺序执行；数据量较大时单阶段可能需要 1–5 分钟，请勿重复点击。")

    # 端到端一键运行
    st.markdown("#### 一键端到端运行")
    if st.button("▶  ingest → clean → events → metrics → diagnose → report",
                 type="primary", width="content"):
        with st.spinner("端到端运行中，请稍候…"):
            result = run_stage("run")
        if result.returncode == 0:
            st.success("端到端运行完成")
            st.cache_data.clear()
        else:
            st.error(f"运行出错（返回码 {result.returncode}）")
        if result.stdout:
            st.code(result.stdout, language="bash")
        if result.stderr:
            st.code(result.stderr, language="bash")

    st.divider()
    st.markdown("#### 逐阶段运行")
    stage_cols = st.columns(len(PIPELINE_STAGES))
    for i, (cmd, label) in enumerate(PIPELINE_STAGES):
        with stage_cols[i]:
            if st.button(label, width="stretch", key=f"stage_{cmd}"):
                with st.spinner(f"{label} 运行中…"):
                    result = run_stage(cmd)
                if result.returncode == 0:
                    st.success("完成")
                    st.cache_data.clear()
                else:
                    st.error("出错")
                if result.stdout:
                    st.code(result.stdout, language="bash")
                if result.stderr:
                    st.code(result.stderr, language="bash")

    st.divider()
    st.markdown("#### 数据目录概况")
    p = paths()
    raw_files  = sum(1 for f in p.raw.rglob("*") if f.is_file() and not f.name.startswith("."))
    int_pqs    = sum(1 for _ in p.interim.glob("*.parquet"))
    proc_pqs   = sum(1 for _ in p.processed.glob("*.parquet"))
    rep_dirs   = sum(1 for _ in p.reports.iterdir() if _.is_dir()) if p.reports.exists() else 0

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("raw/ 源文件数",       raw_files)
    mc2.metric("interim/ parquet",    int_pqs)
    mc3.metric("processed/ parquet",  proc_pqs)
    mc4.metric("reports/ 报告目录数",  rep_dirs)
