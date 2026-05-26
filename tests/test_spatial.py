"""spatial 模块：override 叠加正确性。"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from monitorda.io_paths import paths
from monitorda.spatial import load_network


@pytest.fixture
def temp_overrides(tmp_path, monkeypatch):
    """临时改写 topology_overrides.yaml 路径，测试结束后恢复。"""
    p = paths()
    tmp_yaml = tmp_path / "topology_overrides.yaml"
    yield tmp_yaml
    # cleanup not needed: fixture 作用域内自动消失


def test_load_network_without_shp_uses_sites_yaml():
    # MVP：shp 缺失时仍能加载 19 个节点
    net = load_network()
    # sites.yaml 有 19 个节点
    assert len(net.graph.nodes) >= 19
    assert "W13" in net.graph
    assert "S01" in net.graph


def test_apply_node_flags_override(tmp_path, monkeypatch):
    from monitorda import io_paths
    overrides_path = tmp_path / "topology_overrides.yaml"
    overrides_path.write_text(
        yaml.safe_dump({
            "nodes": {
                "W13": {"flags": {"suspect_illicit": True, "reason": "test"}},
            },
            "links": {"add": [{"from": "W13", "to": "W14", "length_m": 100}]},
            "catchment_overrides": {"W13": {"area_km2_override": 0.5}},
        }, allow_unicode=True),
        encoding="utf-8",
    )

    real_paths = io_paths.paths()
    original = io_paths.Paths(root=real_paths.root)

    class FakePaths:
        def __getattr__(self, name):
            if name == "cfg_topology_overrides":
                return overrides_path
            return getattr(original, name)

    monkeypatch.setattr(io_paths, "paths", lambda: FakePaths())
    # 强制 spatial 模块用新的 paths
    from monitorda import spatial as sp
    monkeypatch.setattr(sp, "paths", lambda: FakePaths())

    net = load_network()
    assert net.graph.nodes["W13"]["flags"]["suspect_illicit"] is True
    assert net.graph.has_edge("W13", "W14")
    assert net.catchment_areas_km2.get("W13") == 0.5


def test_upstream_traversal():
    net = load_network()
    # MVP 无边的情况下，upstream_nodes(W13) 只包含自身
    ups = net.upstream_nodes("W13")
    assert "W13" in ups
