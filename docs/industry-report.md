# 数据 Agent 行业进展与落地判断

研究截止：2026-11-01。以下比较基于 14 条官方/研究资料及本地规范，另增关注账号的6篇公开版本相关章节；未完成微信历史采集。产品能力属于文档证据；本轮未试用这些云服务，未独立验证客户生产效果。

## 可核验的能力与判断

| 场景 | 本轮直接证据 | 水位判断（研究者推论） | 首要落地条件 |
|---|---|---|---|
| 数据研发 | [长任务工程案例](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)、[Spider 2.0](https://spider2-sql.github.io/) | 有可复用工程方法与公开评测；本轮证据不足以证明端到端无人值守研发稳定 | 隔离验证、数据质量、变更审批 |
| 资产检索答疑 | [DataHub MCP](https://docs.datahub.com/docs/features/feature-guides/mcp) | 目录能力已有标准工具入口；适合先做受控辅助检索 | 元数据质量、权限、引用 |
| 数据分析 | [Snowflake](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)、[Genie 监测](https://docs.databricks.com/aws/en/genie-agents/monitor)、[MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow) | 公开产品和语义层集成较清晰；适合限定业务域问数试点 | 批准口径、正确结果、反馈与回归 |
| 数据 Agent | [Google API](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/overview)、[Agent evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | API 和工具编排已可获得；跨域长期可靠执行仍须本地验收 | 状态、预算、终态验证和接管 |

这里不打没有可比依据的统一成熟度分数。厂商支持某能力不表示所有地区/版本/账户可用；采购前用相同保留集、权限和预算做对比。

## 值得注意的变化

当前文档将语义、工具访问和评测放在一起：DataHub 暴露资产上下文，MetricFlow 管指标计算，分析服务提供问答入口，评测服务关注实际结果。由这些公开能力推论，差异化越来越依赖高质量上下文和可验证执行，而非只加一个聊天框。

同时存在产品迁移：Snowflake 当前 Analyst 文档推荐 Cortex Agents；Databricks 文档使用 Genie Agent，注明原 Genie Spaces。实施前应以当前入口和账户可用性为准，避免照搬旧文章步骤。本轮只记录文档变化，未验证迁移成本。

## 投入和价值怎么比较

| 选择 | 主要投入项 | 优势 | 应验证的限制 |
|---|---|---|---|
| 已有平台原生能力 | 接口/推理、查询计算、语义治理、权限联调 | 集成路径短 | 地区、数据驻留、平台依赖、评测结果 |
| 元数据服务加自建工具层 | 元数据运营、接口适配、检索、审计与运维 | 跨平台可控 | 持续维护、人力与权限一致性 |
| 完整自建 Agent 平台 | 上述投入加调度、模型接入、隔离、监控 | 定制空间大 | 可靠性成本、收益是否足够 |

不提供未经核验的单价或节省比例。试点总成本按任务数×平均推理与查询成本，加治理和维护工时估算；另报失败重试、人工审核和错误修复成本。

## 推荐顺序

先资产检索与口径问答，再批准指标的只读分析，然后数据研发建议和 patch，最后才考虑有副作用的执行。优先复用已有目录、调度和权限系统；先证明某个业务域有可量化收益，再扩域或引入完整本体。

本轮没有获得可独立核验的客户生产 SLA、错误率与 ROI 证据，因此这些项保持未知，不以厂商宣传补齐。

## 关注账号公开文章带来的补充

[逐篇发现与边界](followed-account-findings.md)补充了模型准入—组件—业务的评测组织、Spark任务优化闭环、专业数据工具服务以及统一目录与多种检索的产品视角。它们支持继续调查这些实践方向；客户收益、自动进化与准确率等主张仍需独立验证。本轮新增材料没有改变“先语义、权限和评测，再扩大自主执行”的建议。
