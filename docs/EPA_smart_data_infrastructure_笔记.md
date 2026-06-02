# EPA《Smart Data Infrastructure for Wet Weather Control and Decision Support》阅读沉淀

> 原文件：`smart_data_infrastructure_for_wet_weather_control_and_decision_support_-_final_-_august_2018.pdf`
> 来源：美国环保署（U.S. EPA）Office of Wastewater Management；初版 2018-08，本版 2021-03。
> 性质：技术指南 + 22 个案例（Appendix A），全 85 页，定位为 "living document"（持续更新）。
> 主题：如何用"智慧数据基础设施"（监测 + 通信 + 分析）支撑**雨季（wet weather）排水系统的实时控制与决策**。

---

## 一、文档讲了什么（主线）

雨水/融雪（wet weather）会让进入污水处理厂的流量骤增，冲击处理效率与系统安全，并诱发 CSO（合流制溢流）、SSO（污水溢流）、冒溢、内涝。传统应对靠灰色 / 绿色基础设施；本文主张叠加第三条路径——**智慧数据基础设施**：用更便宜更准的传感器 + IoT + 低成本存储 + 无线传输，把系统从"被动反应"转向"主动 / 预测式"运维。

全文按"数据生命周期"组织：

| 章节 | 主题 | 一句话 |
|---|---|---|
| §1–2 | 总览与路线图 | 框架=硬件+通信+管理；可规模化，先小后大；6 步实施路线图 |
| §3 | 信息输入（采集） | 连续监测、液位、流量、降雨四类监测技术与选型 |
| §4 | 收集系统优化 | 离线优化 vs 在线优化（RTC）；CMOM 与 I/I 控制 |
| §5 | RTC 实时控制 | 组件、SCADA、RTDSS、控制层级（本地/区域/全局） |
| §6 | 数据管理与共享 | 大数据治理、网络安全、实时公众通报 |
| §7 | 数据分析 | **数据校验/过滤** + **KPI** |
| §8 | 可视化与 DSS | 决策支持系统三大功能；实时 DSS |
| §9 | 未来展望 | 水质实时传感、预测式运维 |
| Appendix A | 22 个案例 | 见文末清单 |

---

## 二、与本项目（monitorda）强相关的技术要点

monitorda 做的是"排水管网在线监测数据的定期诊断"——离线、回顾性分析（BWF / RDII / Qrl / 时滞 / 节点诊断）。本文虽然侧重**实时控制**，但 §3、§4.1、§7 三块与本项目的方法论高度同源，可作为方法学背书与改进清单。

### 1. 监测数据类型 → 对应 monitorda 的 `data/raw/` 四类
本文 §3 把排水系统"为正常运行需监测的物理量"归纳为：**流量、液位、降雨**，外加设备状态（泵/闸/阀）。这正好对应 monitorda 的四个投放目录：

| 本文监测类型 | monitorda 目录 | 备注 |
|---|---|---|
| Flow monitoring (§3.3) | `nodes_flow/` | 流量 |
| Level monitoring (§3.2) | `nodes_level/` | 液位 |
| Rainfall monitoring (§3.4) | `rainfall/` | 降雨 |
| —（厂区进水） | `plant_inlet/` | 对应 §7 KPI 的 "Treated flow / 进厂流量" |

### 2. 流量数据为何不可全信 → 印证 monitorda "用液位代用流量"的做法
README 方法论表里有一条："液位升幅 / 响应时滞——流量数据失真时的代用指标"。本文给出了量化依据：

- **流量计精度本就有限**：浸没式 ±10%~20%，非接触式 ±15%~30%（24~120 inch 管径实测）。
- 永久流量计单点造价 $15,000~75,000，需每年至少 2 次清洗/校准。
- **液位→流量（Manning 公式）的适用边界**：仅在"自由水面流"成立；**满管承压或顶托（backwater）时失效**。干流误差 <5%，雨天约 15%。
- 校准良好的水力模型（如 EPA SWMM 5）流量精度 −15%~+25%。

> 对 monitorda 的启示：流量列应带"可信度/失真标记"，在满管或顶托工况下自动降级到液位类指标（rise_amp / lag）。这条工程判断本文是支持的。

### 3. I/I 控制（CMOM）→ 直接对应 monitorda 的 RDII / 混接诊断
- **I/I = Inflow（入流）+ Infiltration（入渗）**：非预期的清水（地下水、过量雨水）超出管网设计容量，多因管道老化/失修。
- 本文 §4.1：用**长期流量+液位**分析 I/I 峰值流量与体积的趋势，定位高 I/I 区域、排序整治、做成本效益评估。**这正是 monitorda RDII/Qrl 指标的设计目的。**
- §6.2 提到：机器学习已用于"基于长期趋势的 I/I 特征预测分析"——monitorda 未来可演进方向。
- 术语对照：本文的 **Rainfall-derived I/I** ≈ monitorda 的 **RDII**（雨水诱发的入流入渗）。

### 4. 数据校验与过滤（§7.1）→ 应直接落进 monitorda 的 `clean.py`
本文列出原始监测数据的 6 类典型错误，与清洗模块应处理的异常一一对应：

| 本文错误类型 | 说明 | clean.py 处理建议 |
|---|---|---|
| Noise 噪声 | 高频抖动 | 滤波/平滑 |
| Missing values 缺失 | 通信/校准中断 | gap filling：实时用上一有效值；事后用线性插值 |
| Out of range 越界 | 超传感器/工况范围 | range validation（液位不应低于井底、罕超地面） |
| Outliers 离群 | 突发尖峰 | rate-of-change validation |
| Constant/frozen 冻结 | 传感器故障 | running variance validation（方差过小判失效） |
| Drift 漂移 | 长期偏移 | 期望均值 / 趋势检查；需区分"传感器漂移"还是"真实长期趋势" |

校验方法分两类：**单变量校验**（range / gap fill / rate-of-change / running-variance / drift）与**交叉校验**（cross-validation，利用冗余或软测量/虚拟传感器 + 数据调和）。
> 启示：monitorda 雨量站↔节点（`stations_rainfall.yaml`）、液位↔流量本身就是相关变量，可做交叉校验；这是当前 clean 步骤可补强的点。

### 5. KPI 体系（§7.2）→ 可对照/扩充 monitorda 的 `metrics.py`
本文给出的雨季 KPI（均基于"已校验数据"计算）：

- **Precipitation frequency 降雨频率/重现期**：与 monitorda 事件识别的降雨阈值（`settings.yaml`）呼应；可把各场次最大雨深与重现期对比。
- **Treated flow 进厂流量** vs 处理厂容量 → 对应 `plant_inlet/`。
- **Untreated / Partially treated flow 溢流量**（次数+体积）→ monitorda 可作为节点诊断的上层汇总 KPI。
- **Retention volume / duration 调蓄量与时长**。
- **CSO/SSO volume & duration 溢流体积与时长**。

> monitorda 目前的指标（BWF/RDII/等效混接面积/Qrl/液位升幅/时滞/回落半衰期）更偏"诊断机理"，本文 KPI 更偏"系统绩效"。两者互补——可在报告里增加一层"系统级 KPI 摘要"。

### 6. 降雨监测布点（§3.4）→ 对应 `stations_rainfall.yaml`
- 经验密度：**每 500 公顷（约 1235 英亩）布 1 个雨量计**，依气候与预测精度调整。
- 常用翻斗式雨量计（机械/光学），每翻斗计一固定雨量（如 0.005 inch）。
- 预测窗口/网格应与汇流区最长**汇流时间（time of concentration）**成比例；CSO 类预测至少提前 2 小时。
> 对 monitorda 雨量站→节点分配的合理性是一种背书；可据 500 ha/站 反查覆盖是否足够。

---

## 三、本项目暂不直接用、但值得了解的部分

- **RTC 实时控制（§5）**：monitorda 是离线诊断，不做实时控制。但 RTC 的"本地→区域→全局"控制层级、SCADA 作为 RTC 骨干、RTDSS 叠加在 SCADA 之上做多目标优化（含模型预测控制 MPC）等概念，描绘了"诊断之后"的演进路径——若红旗东路项目后续要做主动调度，可回到 §5。
- **数据管理/网络安全/公众通报（§6）**：偏 IT 架构与合规，与 monitorda 的本地文件流水线关系不大；但"poor/redundant/lost data 可吃掉 15%~25% 运维预算"（USGS）是支持"做好数据治理"的有力论据。
- **可视化与 DSS（§8）**：DSS 三大功能（信息管理 / 数据量化 / 模型操演"what-if"）；monitorda 的 Markdown+DOCX 报告属于最轻量的"信息管理 + 数据量化"，尚无"what-if"场景模拟。

---

## 四、术语速查（与 monitorda 对照）

| 缩写/术语 | 含义 | 与 monitorda 关系 |
|---|---|---|
| I/I (Inflow & Infiltration) | 入流与入渗 | RDII 的上位概念 |
| RDII | 雨水诱发的入流入渗 | monitorda 核心指标 |
| CSO / SSO | 合流制溢流 / 污水溢流 | 诊断后果，可做 KPI |
| CMOM | 容量管理-运行-维护 | I/I 控制的制度框架 |
| BWF (本文未用此缩写) | 旱天基线流量 | monitorda 用 14 天滑窗实现 |
| Manning's Equation | 曼宁公式（液位估流量） | "液位代用流量"的理论依据，满管/顶托失效 |
| Time of Concentration | 汇流时间 | 与时滞 lag、雨量布点相关 |
| KPI | 关键绩效指标 | 报告可增系统级 KPI 层 |
| RTC / RTDSS / SCADA | 实时控制 / 实时决策支持 / 监控采集 | 本项目暂不涉及，属演进方向 |
| Data validation/filtering | 数据校验与过滤 | clean.py 的方法学清单 |

---

## 五、可落地的改进 backlog（来自本文，供后续取舍）

1. **clean.py 增加 6 类异常的显式校验**（noise/missing/out-of-range/outlier/frozen/drift），按本文 §7.1 方法实现；新增交叉校验（液位↔流量、雨量站冗余）。
2. **流量可信度标记**：满管/顶托工况自动降级到液位类指标，与 README "流量失真时用液位代用"形成闭环。
3. **报告增加"系统级 KPI 摘要"层**：降雨重现期、进厂流量/容量比、溢流次数与体积、调蓄量。
4. **雨量布点自检**：按 ~500 ha/站 核查 `stations_rainfall.yaml` 覆盖密度。
5. （远期）若项目走向主动调度，参照 §5 RTC 控制层级与 RTDSS 架构。

---

## 附：Appendix A 的 22 个案例（按主题归类，供需要时回查）

- **CSO 削减 / 内联调蓄优化**：Buffalo NY、Louisville KY（RTC 入选 LTCP 省约 $2 亿）、South Bend IN（2008–2014 CSO 体积降约 70%）、Fort Wayne IN、San Francisco CA、Wilmington DE、Cincinnati OH（"smart sewers"，>200 CSO 点）。
- **内涝 / 洪涝风险**：Beckley WV、Ormond Beach FL（极端事件）、Falcon Heights MN（预测式防洪）、Albany NY。
- **I/I 控制（RTC）**：Grand Rapids MI。
- **溢流监测 / 公众通报**：Green Bay WI、Hawthorne CA、Newburgh NY（无线卫星，公众实时通报）、Rutland VT。
- **维护优化（智能监测降清掏频次）**：La Mesa CA、San Antonio TX（SAWS 试点降清掏频次 94%，零 SSO）。
- **雨水收集/回用、调蓄塘排放**：San Diego CA、Washington DC、Philadelphia PA（承诺 2036 年减溢流 79 亿加仑）。
- **污染与防洪实时控制（海外）**：Bordeaux, France。
