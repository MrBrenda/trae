"""monitorda CLI（Typer）。"""

from __future__ import annotations

from datetime import date
from typing import Optional

import pandas as pd
import typer

from . import __version__
from .io_paths import ensure_dirs, paths

app = typer.Typer(no_args_is_help=True, add_completion=False, help="monitorda — 排水管网诊断流水线")


@app.callback()
def main() -> None:
    """所有子命令前置：确保目录存在。"""
    ensure_dirs()


@app.command()
def version() -> None:
    """打印版本号。"""
    typer.echo(__version__)


@app.command()
def ingest(
    force: bool = typer.Option(False, "--force", help="忽略状态文件，重新解析所有文件"),
) -> None:
    """扫描 data/raw/，解析并合并到 interim parquet。"""
    from .ingest import run_ingest
    summary = run_ingest(force=force)
    if not summary:
        typer.echo("没有发现新数据（或 raw 目录为空）")
        return
    for k, n in summary.items():
        typer.echo(f"  {k:30s}  {n:>10d} rows")


@app.command()
def clean() -> None:
    """对 interim parquet 跑 QC 标记，更新 qc_flag。"""
    from .clean import run_clean
    out = run_clean()
    if not out:
        typer.echo("没有可清洗的 interim parquet")
        return
    for k, v in out.items():
        report = v.get("report", [])
        typer.echo(f"\n=== {k} 可用率 ===")
        for r in report:
            typer.echo(f"  {r['node_id']:5s}  total={r['total']:>6d}  "
                       f"good={r['good']:>6d}  usable={(r['usable_rate'] or 0)*100:>5.1f}%  "
                       f"grade={r['grade']}")


@app.command()
def events() -> None:
    """从 rainfall_hourly 自动识别降雨事件，写 processed/events.parquet。"""
    from .events import detect_events
    from .io_paths import settings as load_settings
    p = paths()
    rain_p = p.parquet("rainfall_hourly")
    if not rain_p.exists():
        typer.echo(f"找不到 {rain_p}，请先运行 ingest")
        raise typer.Exit(1)
    rain_df = pd.read_parquet(rain_p)
    cfg = load_settings().get("events", {})
    ev_df = detect_events(rain_df, **{k: v for k, v in cfg.items()})
    p.processed.mkdir(parents=True, exist_ok=True)
    ev_df.to_parquet(p.parquet("events"), index=False)
    typer.echo(f"识别事件 {len(ev_df)} 场，已写入 {p.parquet('events')}")


@app.command()
def metrics() -> None:
    """计算 BWF / RDII / 时滞 / 升幅 / 半衰期，落 processed/。"""
    from .compute import run_metrics
    out = run_metrics()
    typer.echo(f"BWF 行数: {len(out['bwf'])}, RDII 行数: {len(out['rdii'])}")


@app.command()
def diagnose() -> None:
    """跑节点综合分类，写 processed/node_diagnostics.parquet。"""
    from .diagnose import build_node_diagnostics
    p = paths()
    rdii_p = p.parquet("rdii_by_event_node")
    if not rdii_p.exists():
        typer.echo(f"找不到 {rdii_p}，请先运行 metrics")
        raise typer.Exit(1)
    rdii_df = pd.read_parquet(rdii_p)
    diag = build_node_diagnostics(rdii_df)
    diag.to_parquet(p.parquet("node_diagnostics"), index=False)
    typer.echo(f"诊断 {len(diag)} 个节点，已写入 {p.parquet('node_diagnostics')}")
    for _, d in diag.iterrows():
        typer.echo(f"  {d['node_id']:5s}  {d['name_zh']:20s}  "
                   f"{d['category']:8s}  evidence={d['evidence_score']:.2f}")


@app.command()
def report(
    run_date_str: Optional[str] = typer.Option(None, "--date", help="报告日期 YYYY-MM-DD"),
) -> None:
    """生成 Markdown + DOCX 报告到 reports/<date>/。"""
    from .figures import node_rise_amp_bar, plant_inlet_timeseries, site_map
    from .report_docx import render_docx
    from .report_md import render_report

    rd = date.fromisoformat(run_date_str) if run_date_str else date.today()
    p = paths()
    run_dir = p.report_dir(rd)
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)

    plant_df = pd.read_parquet(p.parquet("plant_inlet_10min")) if p.parquet("plant_inlet_10min").exists() else pd.DataFrame()
    events_df = pd.read_parquet(p.parquet("events")) if p.parquet("events").exists() else pd.DataFrame()
    rdii_df = pd.read_parquet(p.parquet("rdii_by_event_node")) if p.parquet("rdii_by_event_node").exists() else pd.DataFrame()
    diag_df = pd.read_parquet(p.parquet("node_diagnostics")) if p.parquet("node_diagnostics").exists() else pd.DataFrame()

    plant_inlet_timeseries(plant_df, events_df, run_dir / "figures" / "plant_inlet.png")
    node_rise_amp_bar(rdii_df, run_dir / "figures" / "node_rise_amp.png")
    site_map(diag_df, run_dir / "figures" / "site_map.png")

    md = render_report(run_dir, run_date=rd)
    dx = render_docx(run_dir, run_date=rd)
    typer.echo(f"已生成：\n  {md}\n  {dx}")


@app.command()
def run(
    since: Optional[str] = typer.Option(None, "--since", help="不参与计算，仅用于元数据"),
    until: Optional[str] = typer.Option(None, "--until"),
) -> None:
    """端到端：ingest → clean → events → metrics → diagnose → report。"""
    typer.echo(">>> 1/6 ingest")
    ingest(force=False)
    typer.echo(">>> 2/6 clean")
    clean()
    typer.echo(">>> 3/6 events")
    events()
    typer.echo(">>> 4/6 metrics")
    metrics()
    typer.echo(">>> 5/6 diagnose")
    diagnose()
    typer.echo(">>> 6/6 report")
    report(run_date_str=None)
    typer.echo("\n完成。")


@app.command()
def verify(
    against: str = typer.Option("tests/expected_0423.yaml", "--against", help="期望值 YAML 路径"),
) -> None:
    """与期望值对照，打印差异表。"""
    import yaml
    from pathlib import Path
    p = paths()
    exp_path = Path(against)
    if not exp_path.is_absolute():
        exp_path = p.root / exp_path
    if not exp_path.exists():
        typer.echo(f"找不到期望值文件：{exp_path}")
        raise typer.Exit(1)
    expected = yaml.safe_load(exp_path.read_text(encoding="utf-8"))
    rdii_df = pd.read_parquet(p.parquet("rdii_by_event_node")) if p.parquet("rdii_by_event_node").exists() else pd.DataFrame()

    rows = []
    for ev_id, nodes in (expected.get("rdii") or {}).items():
        for nid, fields in (nodes or {}).items():
            actual = rdii_df[(rdii_df["event_id"] == ev_id) & (rdii_df["node_id"] == nid)]
            if actual.empty:
                rows.append({"event": ev_id, "node": nid, "field": "*", "expected": "—", "actual": "missing"})
                continue
            r = actual.iloc[0]
            for f, exp_v in fields.items():
                rows.append({
                    "event": ev_id, "node": nid, "field": f,
                    "expected": exp_v,
                    "actual": r.get(f),
                })
    if not rows:
        typer.echo("期望值为空，跳过校验")
        return
    df = pd.DataFrame(rows)
    typer.echo(df.to_string(index=False))


if __name__ == "__main__":
    app()
