# monitorda - 排水管网监测数据诊断工作流

PYTHON ?= python3
VENV   ?= .venv
PIP    := $(VENV)/bin/pip
PY     := $(VENV)/bin/python
MON    := $(VENV)/bin/monitorda

.PHONY: help venv install dev-install app-install app test test-cov lint fmt clean run report verify-0423 ingest events diagnose

help:
	@echo "Available targets:"
	@echo "  make venv          - create .venv with Python 3.11+"
	@echo "  make install       - install runtime deps (editable)"
	@echo "  make dev-install   - install runtime + dev deps"
	@echo "  make app-install   - install app extras (streamlit + plotly)"
	@echo "  make app           - launch Streamlit dashboard (http://localhost:8501)"
	@echo "  make run           - end-to-end pipeline (today's window)"
	@echo "  make report        - re-render report from latest processed"
	@echo "  make ingest        - scan data/raw/ and merge into interim"
	@echo "  make events        - re-detect storm events"
	@echo "  make diagnose      - re-run diagnosis"
	@echo "  make verify-0423   - regression test against 0423 docx values"
	@echo "  make test          - run unit + regression tests"
	@echo "  make lint          - ruff + black --check"
	@echo "  make fmt           - black + ruff --fix"
	@echo "  make clean         - remove caches and build artefacts"

venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools wheel

install: venv
	$(PIP) install -e .

dev-install: venv
	$(PIP) install -e ".[dev]"

app-install: venv
	$(PIP) install -e ".[app]"

app: venv
	echo "" | STREAMLIT_BROWSER_GATHER_USAGE_STATS=false $(VENV)/bin/streamlit run app/streamlit_app.py

run:
	$(MON) run

report:
	$(MON) report

ingest:
	$(MON) ingest

events:
	$(MON) events

diagnose:
	$(MON) diagnose

verify-0423:
	$(VENV)/bin/pytest -m regression -v

test:
	$(VENV)/bin/pytest

test-cov:
	$(VENV)/bin/pytest --cov=monitorda --cov-report=term-missing

lint:
	$(VENV)/bin/ruff check src tests
	$(VENV)/bin/black --check src tests

fmt:
	$(VENV)/bin/ruff check --fix src tests
	$(VENV)/bin/black src tests

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
