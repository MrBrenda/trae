# monitorda — 排水管网在线监测数据定期诊断工作流

把《红旗东路积涝整治及管网改造专题研究阶段性成果报告 0423》中体现的方法论沉淀为 Python 流水线：
新一期数据投放 → 自动清洗 → 事件识别 → BWF/RDII/Qrl/时滞计算 → 节点诊断 → Markdown + DOCX 报告。

> 科学正确性以 0423 docx 为回归基准，详见 `tests/expected_0423.yaml`。

## 快速开始

```bash
# 1. 准备环境
make dev-install

# 2. 准备数据
#   把监测数据按类别拷入 data/raw/{plant_inlet,nodes_flow,nodes_level,rainfall}/
#   把站点表 sites.xlsx 与管网 network.shp 放入 data/external/

# 3. 跑一条命令完成端到端诊断
make run
# 等价于：monitorda ingest && monitorda clean && monitorda events && \
#         monitorda metrics && monitorda diagnose && monitorda report

# 4. 查看产物
open reports/$(date +%F)/report.md
open reports/$(date +%F)/report.docx
```

## 项目结构

```
data/                       用户数据区
├── raw/                    新数据投放点（plant_inlet / nodes_flow / nodes_level / rainfall）
├── interim/                清洗后的 parquet（按 node_id / year_month 分区）
├── processed/              事件级 + 诊断结果（parquet + csv）
└── external/               站点 Excel、管网 shp 等只读参考数据

config/
├── settings.yaml           降雨阈值、BWF 窗口、C 范围、容差
├── sites.yaml              S01–S10 / W11–W19 ↔ 中文名映射
├── topology_overrides.yaml shp 之上的纠错 patch 层
└── stations_rainfall.yaml  雨量站 → 节点分配

src/monitorda/
├── ingest.py  clean.py  events.py  metrics.py
├── spatial.py  diagnose.py
├── report_md.py  report_docx.py
├── schema.py  io_paths.py  cli.py
└── templates/              jinja2 + docx 模板

reports/<run-date>/         每次运行产出独立目录
tests/                      单元测试 + 0423 回归测试
```

## 方法论一览

| 概念 | 实现位置 | 0423 报告对照 |
|---|---|---|
| 旱天基线 BWF | `metrics.bwf` | 14 天滑动窗口 ±14d |
| RDII 体积 | `metrics.rdii` | 事件期 + 48h 回落尾 减 BWF |
| 等效混接面积 km² | `metrics.equivalent_illicit_area` | V/(C·P·1000), C=0.78–0.90 |
| Qrl 雨水入流评定 | `metrics.qrl` | Σ(RDII/R)/Σ(L) |
| 液位升幅 / 响应时滞 | `metrics.rise_amp` / `lag_start` / `lag_peak` | 流量数据失真时的代用指标 |
| 回落半衰期 | `metrics.recession_halflife` | 区分入流 vs 入渗 |
| 节点诊断分类 | `diagnose.classify` | 混接 / 入渗 / 直连 / 雨水管低效 |

## 节点 ID 规范

- **雨水节点**：`S01` – `S10`（对应原报告"节点1"–"节点10"）
- **污水节点**：`W11` – `W19`（对应原报告"节点11"–"节点19"）
- 中文名 / 道路位置 / 坐标维护在 `config/sites.yaml`

## 数据来源约定

监测数据由用户从平台手动导出后拷入 `data/raw/` 对应子目录。文件命名建议（不强制）：

```
data/raw/plant_inlet/5wwtp_2026-04.xlsx
data/raw/nodes_level/W13_2026-04.csv
data/raw/nodes_flow/W13_2026-04.csv
data/raw/rainfall/V8805_2026-04.csv
```

`monitorda ingest` 自动识别文件类型与节点 ID，去重合并到 `data/interim/` 下的 parquet。

## 拓扑纠错

`data/external/network.shp` 是 source-of-truth（只读）。后期发现的拓扑/属性错误，写入 `config/topology_overrides.yaml`：

```yaml
nodes:
  W14:
    flags: { suspect_illicit: true, reason: "现场 2026-03 复核" }
links:
  set:
    - { from: W15, to: W16, attrs: { length_m: 215 } }
```

`spatial.load_network()` 会在加载时叠加 patch，shp 文件本身永远不动。

## 验证

```bash
make verify-0423      # 回归 0423 报告的 5 事件 × 19 节点结论
make test             # 全部单元测试
make lint             # ruff + black --check
```

## 0423 报告对照

参见 [`reports/_reference_0423.md`](reports/_reference_0423.md)（如已生成）或仓库根目录的 docx 原件。
