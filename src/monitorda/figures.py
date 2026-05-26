"""图表生成：MVP 阶段优先两张关键图。"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # 无 GUI 后端
import matplotlib.pyplot as plt
import pandas as pd

# 中文显示
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "STHeiti", "Songti SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def plant_inlet_timeseries(
    plant_df: pd.DataFrame,
    events_df: pd.DataFrame,
    out_path: Path,
) -> Path:
    """污水厂入流时间序列，叠加事件窗口阴影。"""
    fig, ax = plt.subplots(figsize=(10, 4), dpi=120)
    if not plant_df.empty and "flow_m3s" in plant_df.columns:
        ax.plot(plant_df["ts"], plant_df["flow_m3s"], lw=0.5, label="入流流量 m³/s")
    if not events_df.empty:
        for _, ev in events_df.iterrows():
            ax.axvspan(ev["t_start"], ev["t_end"], color="orange", alpha=0.2)
    ax.set_xlabel("时间")
    ax.set_ylabel("流量 m³/s")
    ax.set_title("第五污水厂入流时间序列（橙色阴影为降雨事件）")
    ax.legend(loc="best")
    fig.autofmt_xdate()
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


def node_rise_amp_bar(
    rdii_df: pd.DataFrame,
    out_path: Path,
) -> Path:
    """每节点中位升幅条形图 — 表 4.4 的可视化对应。"""
    if rdii_df.empty:
        # 占位空图
        fig, ax = plt.subplots(figsize=(8, 4), dpi=120)
        ax.text(0.5, 0.5, "无 RDII 数据", ha="center", va="center")
        ax.axis("off")
    else:
        agg = (rdii_df.dropna(subset=["rise_amp_m"])
               .groupby("node_id")["rise_amp_m"].median()
               .sort_values())
        fig, ax = plt.subplots(figsize=(10, 5), dpi=120)
        colors = ["#d62728" if v >= 3.0 else ("#ff7f0e" if v >= 1.0 else "#2ca02c") for v in agg.values]
        ax.barh(agg.index, agg.values, color=colors)
        ax.set_xlabel("液位中位升幅 m")
        ax.set_title("各节点雨天响应升幅（RDII 强度代理指标）")
        ax.axvline(3.0, color="gray", linestyle="--", lw=0.5)
        ax.axvline(1.0, color="gray", linestyle=":", lw=0.5)
        fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


def site_map(
    diag_df: pd.DataFrame,
    out_path: Path,
) -> Path:
    """监测点位空间分布 — 若 sites.yaml 含坐标则按坐标画，否则按 node_id 字母分布。

    分类用颜色编码：混接(红)/入渗(橙)/直连(深红)/雨水管低效(蓝)/未定(灰)/数据不足(浅灰)。
    """
    from .io_paths import sites as load_sites
    site_cfg = (load_sites().get("nodes") or {})

    points = []
    for nid, info in site_cfg.items():
        lon = info.get("lon")
        lat = info.get("lat")
        if lon is not None and lat is not None:
            points.append({"node_id": nid, "lon": float(lon), "lat": float(lat),
                           "kind": info.get("kind", "sewage")})

    fig, ax = plt.subplots(figsize=(8, 8), dpi=120)
    if not points:
        ax.text(0.5, 0.5, "缺少坐标信息\n请在 sites.yaml 或 sites.xlsx 中补充",
                ha="center", va="center")
        ax.axis("off")
    else:
        df = pd.DataFrame(points)
        if not diag_df.empty:
            df = df.merge(diag_df[["node_id", "category"]], on="node_id", how="left")
        color_map = {
            "混接": "#d62728", "入渗": "#ff7f0e", "直连": "#8b0000",
            "雨水管低效": "#1f77b4", "未定": "#7f7f7f", "数据不足": "#cccccc",
        }
        for cat, sub in df.groupby("category", dropna=False):
            c = color_map.get(cat, "#7f7f7f")
            ax.scatter(sub["lon"], sub["lat"], c=c, label=str(cat), s=80, edgecolors="black", linewidths=0.5)
            for _, row in sub.iterrows():
                ax.annotate(row["node_id"], (row["lon"], row["lat"]),
                            fontsize=8, xytext=(4, 4), textcoords="offset points")
        ax.set_xlabel("经度")
        ax.set_ylabel("纬度")
        ax.set_title("监测节点空间分布与诊断类别")
        ax.legend(loc="best", fontsize=9)
        ax.set_aspect("equal", adjustable="datalim")
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)
    return out_path
