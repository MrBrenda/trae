"""空间模块：shp 加载 + YAML override 叠加 + 拓扑图运算。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import networkx as nx

from .io_paths import paths, sites, topology_overrides


# ---------------------------------------------------------------------------
# 网络解析
# ---------------------------------------------------------------------------

@dataclass
class ResolvedNetwork:
    graph: nx.DiGraph = field(default_factory=nx.DiGraph)
    catchment_areas_km2: dict[str, float] = field(default_factory=dict)
    provenance: list[str] = field(default_factory=list)

    def upstream_nodes(self, node_id: str) -> list[str]:
        """返回 node_id 的所有上游节点（含自身）。"""
        if node_id not in self.graph:
            return []
        return list(nx.ancestors(self.graph, node_id)) + [node_id]

    def downstream_nodes(self, node_id: str) -> list[str]:
        if node_id not in self.graph:
            return []
        return list(nx.descendants(self.graph, node_id)) + [node_id]

    def contributing_area(self, node_id: str) -> float | None:
        """节点的上游汇水面积合计（km²）。"""
        ups = self.upstream_nodes(node_id)
        if not ups:
            return None
        total = 0.0
        any_known = False
        for n in ups:
            a = self.catchment_areas_km2.get(n)
            if a is not None:
                total += a
                any_known = True
        return total if any_known else None

    def distance_along_pipe(self, a: str, b: str) -> float | None:
        """沿管网从 a 到 b 的累计长度（m）。需 graph 中边带 length_m 属性。"""
        if a not in self.graph or b not in self.graph:
            return None
        try:
            path = nx.shortest_path(self.graph, a, b, weight="length_m")
        except nx.NetworkXNoPath:
            return None
        total = 0.0
        for u, v in zip(path[:-1], path[1:]):
            total += float(self.graph[u][v].get("length_m", 0.0))
        return total


def load_network(shp_path: Path | None = None) -> ResolvedNetwork:
    """加载 network.shp（若存在）并叠加 override 层，返回 ResolvedNetwork。

    MVP 实现策略：shp 缺失时，仅以 sites.yaml 构造孤立节点；override 全量生效。
    后续可扩展 shp 解析逻辑。
    """
    g = nx.DiGraph()
    prov: list[str] = []

    # 1) 节点：先从 sites.yaml 灌入
    s = sites()
    for nid, meta in (s.get("nodes") or {}).items():
        g.add_node(nid, **meta)
    prov.append(f"loaded {len(g)} nodes from sites.yaml")

    # 2) shp：MVP 阶段提供占位加载
    if shp_path is None:
        shp_path = paths().network_shp
    if shp_path and shp_path.exists():
        try:
            import geopandas as gpd
            gdf = gpd.read_file(shp_path)
            # 假定 shp 字段含 from_node / to_node / length_m / diameter_m（用户的 shp schema 后续可调）
            from_col = _first_col(gdf, ["from_node", "from", "起始节点", "上游节点"])
            to_col = _first_col(gdf, ["to_node", "to", "终止节点", "下游节点"])
            len_col = _first_col(gdf, ["length_m", "length", "管长"])
            dia_col = _first_col(gdf, ["diameter_m", "diameter", "管径"])
            if from_col and to_col:
                added = 0
                for _, row in gdf.iterrows():
                    u, v = str(row[from_col]), str(row[to_col])
                    if not u or not v or u == "nan" or v == "nan":
                        continue
                    attrs: dict[str, Any] = {}
                    if len_col:
                        attrs["length_m"] = float(row[len_col]) if row[len_col] is not None else 0.0
                    if dia_col:
                        attrs["diameter_m"] = float(row[dia_col]) if row[dia_col] is not None else None
                    g.add_edge(u, v, **attrs)
                    added += 1
                prov.append(f"loaded {added} edges from {shp_path.name}")
            else:
                prov.append(f"warning: {shp_path.name} 缺少 from/to 节点列，未导入边")
        except Exception as e:  # noqa: BLE001
            prov.append(f"warning: shp 加载失败 ({e}); 仅使用 override")
    else:
        prov.append(f"info: {shp_path} 不存在，仅使用 sites.yaml + overrides")

    # 3) 叠加 overrides
    ov = topology_overrides()
    catchments: dict[str, float] = {}

    for nid, patch in (ov.get("nodes") or {}).items():
        if "add" in patch:
            if nid not in g:
                g.add_node(nid)
            for k, v in patch["add"].items():
                g.nodes[nid][k] = v
        if "set" in patch:
            if nid not in g:
                g.add_node(nid)
            for k, v in patch["set"].items():
                g.nodes[nid][k] = v
        if "flags" in patch:
            flags = g.nodes.get(nid, {}).get("flags", {}) or {}
            flags.update(patch["flags"])
            g.add_node(nid, flags=flags)
    prov.append(f"applied {len(ov.get('nodes') or {})} node overrides")

    links = ov.get("links") or {}
    for ln in links.get("add", []) or []:
        g.add_edge(ln["from"], ln["to"], **{k: v for k, v in ln.items() if k not in {"from", "to"}})
    for ln in links.get("remove", []) or []:
        if g.has_edge(ln["from"], ln["to"]):
            g.remove_edge(ln["from"], ln["to"])
    for ln in links.get("set", []) or []:
        if g.has_edge(ln["from"], ln["to"]):
            attrs = ln.get("attrs", {}) or {}
            for k, v in attrs.items():
                g[ln["from"]][ln["to"]][k] = v
    prov.append(f"applied link overrides: +{len(links.get('add') or [])} -{len(links.get('remove') or [])} ~{len(links.get('set') or [])}")

    for nid, patch in (ov.get("catchment_overrides") or {}).items():
        if "area_km2_override" in patch:
            catchments[nid] = float(patch["area_km2_override"])
    prov.append(f"applied {len(catchments)} catchment overrides")

    return ResolvedNetwork(graph=g, catchment_areas_km2=catchments, provenance=prov)


def _first_col(gdf, names: list[str]) -> str | None:
    cols = {str(c).lower(): c for c in gdf.columns}
    for n in names:
        if n.lower() in cols:
            return cols[n.lower()]
    return None


# ---------------------------------------------------------------------------
# 站点 → 节点的雨量分配
# ---------------------------------------------------------------------------

def station_for_node(node_id: str) -> str | None:
    from .io_paths import stations_rainfall
    cfg = stations_rainfall()
    ass = (cfg.get("assignments") or {}).get(node_id)
    if not ass:
        return None
    return ass.get("primary")
