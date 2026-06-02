# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`monitorda` is a batch pipeline that turns periodically-exported drainage-network monitoring data (plant inlet / node flow / node level / rainfall) into a diagnostic report. It operationalizes the methodology of the report `红旗东路积涝整治及管网改造专题研究阶段性成果报告0423.docx` (in repo root). **That docx is the scientific ground truth** — the `regression`-marked tests in `tests/` and `tests/expected_0423.yaml` exist to keep the code reproducing its 5-event × 19-node conclusions. When changing any metric or threshold, run the regression suite and treat divergence from 0423 as a defect unless intentionally revising the method.

## Commands

```bash
make dev-install      # create .venv (Python 3.11–3.12) + install -e ".[dev]"
make run              # end-to-end: ingest → clean → events → metrics → diagnose → report
make test             # full pytest suite
make verify-0423      # only the @regression tests (pytest -m regression)
make lint             # ruff check + black --check (line-length 100)
make fmt              # ruff --fix + black
```

Single test / single stage:
```bash
.venv/bin/pytest tests/test_metrics.py::test_name -v
.venv/bin/monitorda metrics          # run one pipeline stage; same subcommands as the 6 run steps
.venv/bin/monitorda verify --against tests/expected_0423.yaml   # print a diff table vs expected (no assert)
```

The CLI is the entry point for everything: `monitorda {ingest,clean,events,metrics,diagnose,report,run,verify,version}` (Typer app at `monitorda.cli:app`). Each stage reads/writes parquet and can be run independently as long as upstream parquet exists.

## Architecture

### Pipeline = 6 stages over a parquet data lake

Data flows through `data/` in one direction, each stage consuming the previous stage's parquet:

```
data/raw/{plant_inlet,nodes_flow,nodes_level,rainfall}/   ← user drops exported files here
  └─ ingest  → data/interim/*.parquet   (plant_inlet_10min, node_level_10min, node_flow_10min, rainfall_hourly)
  └─ clean   → updates qc_flag in-place on interim parquet
  └─ events  → data/processed/events.parquet
  └─ metrics → data/processed/{bwf_by_node, rdii_by_event_node}.parquet
  └─ diagnose→ data/processed/node_diagnostics.parquet
  └─ report  → reports/<date>/{report.md, report.docx, figures/}
```

`io_paths.py` is the **single source of truth for every path** — never hardcode paths elsewhere. `paths().parquet(kind)` routes a logical table name to interim vs processed automatically. `Paths.root` is resolved by walking up to the dir containing `pyproject.toml`.

### Config-driven, not code-driven

All numeric thresholds live in `config/*.yaml`, never in code. Tuning is meant to happen in YAML:
- `settings.yaml` — every threshold (event detection, BWF window, RDII tail, runoff coefficients, diagnosis cutoffs, QC rules, regression tolerances). `metrics`/`diagnose`/`events` read their sub-dicts.
- `sites.yaml` — the node registry. Node IDs are canonical: **`S01`–`S10` = stormwater, `W11`–`W19` = sewage** (maps to "节点1"–"节点19" via `orig_index`). The `nodes` keys here drive which nodes `compute.py` iterates.
- `stations_rainfall.yaml` — rain-station → node assignment; `spatial.station_for_node()` picks each node's `primary` station to window its events.
- `topology_overrides.yaml` — patch layer over `network.shp` (add/set/remove nodes, links, catchment areas). **The shp is read-only**; corrections go here.

`io_paths.settings()/sites()/stations_rainfall()` are `@lru_cache`d (loaded once per process). `topology_overrides()` is intentionally **not** cached — it is re-read each call so edits take effect mid-run.

### Schema contract

`schema.py` defines pandera `DataFrameSchema`s for every table. The controlled vocabularies there are the contract the whole pipeline relies on:
- `qc_flag ∈ {good, null, stuck0, impossible, outlier, communication_loss}` — downstream compute filters to `qc_flag == "good"` only.
- `category ∈ {混接, 入渗, 直连, 雨水管低效, 未定, 数据不足}` — the diagnosis output classes.
- node_id must match `^[SW]\d{2}$`.

### Metrics layer (the science)

`metrics.py` holds the per-event/per-node primitives (`bwf`, `rdii`, `rise_amp`, `lag_start`, `lag_peak`, `recession_halflife`, `equivalent_illicit_area`). `compute.py` orchestrates them across all (node × event) pairs and writes the two processed tables.

Critical behavior to preserve when editing `compute.py`:
- **Flow is preferred; level is the fallback proxy.** Node flow data is often distorted/missing. When flow is absent, BWF/lag/halflife are computed from `level_m` instead, and RDII *volume* (`v_rdii_m3`) is simply not computed (left `None`) — only level-based indicators (`rise_amp_m`, lags) are. Don't assume flow exists.
- `qrl` is left `None` at the single-node/single-event level by design — it is a cross-node aggregate computed later, not per row.
- BWF (dry-weather baseline) uses a ±`window_days` window around each event but **excludes** any data within `exclude_radius_h` of *any other* event, and requires `min_samples`.

### Diagnosis logic

`diagnose.py::classify()` is the rule engine mapping aggregated stats → a `category`. The rules encode the 0423 report's reasoning (see the module docstring): short lag + large rise → 直连/混接 (inflow); long recession halflife + low/mid rise → 入渗 (infiltration); weak wet-weather response on a stormwater node → 雨水管低效. It short-circuits to 数据不足 when `n_events < 2` or `usable_rate < 0.3`. Stormwater vs sewage nodes follow different branches (gated on `site_kind`). All cutoffs come from `settings.yaml: diagnose`.

### Spatial / network

`spatial.load_network()` returns a `ResolvedNetwork` (a `networkx.DiGraph`) built by: seeding nodes from `sites.yaml` → optionally loading edges from `network.shp` (graceful if missing/malformed) → applying `topology_overrides.yaml`. It exposes `upstream_nodes`, `contributing_area`, `distance_along_pipe`. The shp loader is MVP-level (column-name heuristics); absence of the shp is a supported state, not an error.

### Ingest is heuristic by necessity

Source platforms export inconsistent formats, so `ingest.py` classifies files by **subdirectory** (`raw/<kind>/`), extracts `node_id`/`station_id` from filename or in-table columns via regex, and maps arbitrary column names to the canonical schema via alias lists (`*_FIELD_ALIASES`). It tries multiple encodings (utf-8/gbk/...). Ingest is incremental and idempotent: `data/_ingest_state.json` tracks each file's sha256, so re-running skips unchanged files (`--force` to override). `upsert_parquet` dedupes on natural keys (`DEDUPE_KEYS`), keeping the latest.

## Conventions & gotchas

- Regression tests are `@pytest.mark.regression` and **auto-skip when `data/raw/` is empty** — they need real data present. `make test` on a fresh clone passes by skipping them; that is expected, not a green light that the science is verified.
- `data/` and `reports/` contents are gitignored (only `.gitkeep`); the pipeline regenerates everything from `data/raw/` + `config/`.
- Code, comments, and report output are in Chinese — match that when editing.
- DOCX/PDF reading is intercepted by a global markitdown hook: a `Read` on a `.docx`/`.pdf`/etc. is auto-converted to Markdown under `docs/_converted/` and you're redirected there. To inspect the 0423 docx baseline, just `Read` it and follow the redirect.
