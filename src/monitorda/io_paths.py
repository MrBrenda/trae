"""路径管理。所有读写路径的唯一来源。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path

import yaml


def project_root() -> Path:
    """项目根目录（包含 pyproject.toml 的目录）。"""
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("未找到 pyproject.toml，无法定位项目根目录")


@dataclass(frozen=True)
class Paths:
    root: Path

    @property
    def data(self) -> Path:
        return self.root / "data"

    @property
    def raw(self) -> Path:
        return self.data / "raw"

    @property
    def raw_plant(self) -> Path:
        return self.raw / "plant_inlet"

    @property
    def raw_nodes_flow(self) -> Path:
        return self.raw / "nodes_flow"

    @property
    def raw_nodes_level(self) -> Path:
        return self.raw / "nodes_level"

    @property
    def raw_rainfall(self) -> Path:
        return self.raw / "rainfall"

    @property
    def interim(self) -> Path:
        return self.data / "interim"

    @property
    def processed(self) -> Path:
        return self.data / "processed"

    @property
    def external(self) -> Path:
        return self.data / "external"

    @property
    def ingest_state(self) -> Path:
        return self.data / "_ingest_state.json"

    @property
    def network_shp(self) -> Path:
        return self.external / "network.shp"

    @property
    def sites_xlsx(self) -> Path:
        return self.external / "sites.xlsx"

    @property
    def catchments_shp(self) -> Path:
        return self.external / "catchments.shp"

    @property
    def network_resolved_gpkg(self) -> Path:
        return self.interim / "network_resolved.gpkg"

    @property
    def config(self) -> Path:
        return self.root / "config"

    @property
    def cfg_settings(self) -> Path:
        return self.config / "settings.yaml"

    @property
    def cfg_sites(self) -> Path:
        return self.config / "sites.yaml"

    @property
    def cfg_topology_overrides(self) -> Path:
        return self.config / "topology_overrides.yaml"

    @property
    def cfg_stations(self) -> Path:
        return self.config / "stations_rainfall.yaml"

    @property
    def reports(self) -> Path:
        return self.root / "reports"

    def report_dir(self, run_date: date | None = None) -> Path:
        d = (run_date or date.today()).isoformat()
        return self.reports / d

    # 标准 interim 表
    def parquet(self, kind: str) -> Path:
        """kind ∈ {plant_inlet_10min, node_level_10min, node_flow_10min,
        rainfall_hourly, events, bwf_by_node, rdii_by_event_node, node_diagnostics, rtk_by_node}"""
        if kind in {"events", "bwf_by_node", "rdii_by_event_node", "node_diagnostics", "rtk_by_node"}:
            return self.processed / f"{kind}.parquet"
        return self.interim / f"{kind}.parquet"


@lru_cache(maxsize=1)
def paths() -> Paths:
    return Paths(root=project_root())


@lru_cache(maxsize=1)
def settings() -> dict:
    with paths().cfg_settings.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def sites() -> dict:
    with paths().cfg_sites.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def stations_rainfall() -> dict:
    with paths().cfg_stations.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def topology_overrides() -> dict:
    """非缓存：用户可能在运行中修改此文件，每次重新读取。"""
    p = paths().cfg_topology_overrides
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def ensure_dirs() -> None:
    """确保所有运行时目录存在。"""
    p = paths()
    for d in [p.raw, p.raw_plant, p.raw_nodes_flow, p.raw_nodes_level, p.raw_rainfall,
              p.interim, p.processed, p.external, p.reports]:
        d.mkdir(parents=True, exist_ok=True)
