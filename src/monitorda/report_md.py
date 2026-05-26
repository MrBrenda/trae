"""Markdown 报告生成。"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .io_paths import paths


def _env() -> Environment:
    tpl_dir = Path(__file__).parent / "templates"
    return Environment(
        loader=FileSystemLoader(tpl_dir),
        autoescape=select_autoescape(["html"]),
        trim_blocks=False,
        lstrip_blocks=False,
    )


def render_report(
    run_dir: Path,
    *,
    run_date: date | None = None,
    window_start: str | None = None,
    window_end: str | None = None,
) -> Path:
    p = paths()
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "figures").mkdir(exist_ok=True)
    (run_dir / "tables").mkdir(exist_ok=True)

    events_df = _safe_read(p.parquet("events"))
    rdii_df = _safe_read(p.parquet("rdii_by_event_node"))
    diag_df = _safe_read(p.parquet("node_diagnostics"))
    level_df = _safe_read(p.parquet("node_level_10min"))

    quality_table = _quality_summary(level_df)

    events_table = events_df.to_dict(orient="records") if not events_df.empty else []
    # 时间戳转字符串
    for e in events_table:
        for k in ("t_start", "t_end", "t_peak"):
            if k in e and e[k] is not None:
                e[k] = str(pd.Timestamp(e[k]))

    rdii_grades = []
    if not diag_df.empty:
        for _, d in diag_df.iterrows():
            rdii_grades.append({
                "node_id": d["node_id"],
                "name_zh": d["name_zh"],
                "kind": d["kind"],
                "rise_amp_m": d.get("mean_rise_amp_m"),
                "lag_start_h": d.get("median_lag_start_h"),
                "halflife_h": d.get("median_halflife_h"),
                "grade": _grade_from_rise(d.get("mean_rise_amp_m")),
            })

    # 落表 CSV
    if not events_df.empty:
        events_df.to_csv(run_dir / "tables" / "events.csv", index=False, encoding="utf-8-sig")
    if not rdii_df.empty:
        rdii_df.to_csv(run_dir / "tables" / "rdii_by_event_node.csv", index=False, encoding="utf-8-sig")
    if not diag_df.empty:
        diag_df.to_csv(run_dir / "tables" / "node_diagnostics.csv", index=False, encoding="utf-8-sig")

    env = _env()
    tpl = env.get_template("report.md.j2")
    ctx = {
        "run_date": (run_date or date.today()).isoformat(),
        "window_start": window_start or "(全量)",
        "window_end": window_end or "(全量)",
        "n_nodes": int(diag_df.shape[0]) if not diag_df.empty else 0,
        "n_events": int(events_df.shape[0]) if not events_df.empty else 0,
        "quality_table": quality_table,
        "events_table": events_table,
        "rdii_grades": rdii_grades,
        "diagnostics": diag_df.to_dict(orient="records") if not diag_df.empty else [],
    }
    md = tpl.render(**ctx)
    out = run_dir / "report.md"
    out.write_text(md, encoding="utf-8")
    return out


def _safe_read(p: Path) -> pd.DataFrame:
    return pd.read_parquet(p) if p.exists() else pd.DataFrame()


def _quality_summary(level_df: pd.DataFrame) -> list[dict]:
    if level_df.empty or "node_id" not in level_df.columns:
        return []
    from .clean import null_rate_report
    df = null_rate_report(level_df, "level_m")
    return df.to_dict(orient="records")


def _grade_from_rise(rise: float | None) -> str:
    from .diagnose import grade_rdii
    return grade_rdii(rise)
