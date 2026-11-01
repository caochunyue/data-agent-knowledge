# 工具与接法：优先复用 MaxCompute、Dataphin 和内网能力

本页基于 2026-11-01 可核验的公开官方资料和项目环境背景。公开文档证明产品存在某项能力，不证明公司版本、租户、接口或权限已开放。落地第一步是由平台同学确认版本、许可、API、网络和最小权限。

## 推荐组合

| 环节 | 默认路线 | 备选/扩展 | 输入 → 输出 | 关键限制与替换条件 |
|---|---|---|---|---|
| 资产获取 | Dataphin 作为资产、血缘和负责人来源，优先官方授权接口；否则做有限导出 | 现有内部元数据服务；若未来跨平台再评估 [DataHub](https://docs.datahub.com/docs/features/feature-guides/mcp) | 资产 ID/关键词 → schema、血缘、任务、负责人、采集时间 | Dataphin 公开 API 有表血缘查询，但公司版本和授权需确认；不能抓页面或复制全库绕过权限 |
| SQL/作业分析 | 现有生产 SQL 与 Dataphin 作业为权威实现，MaxCompute EXPLAIN 辅助计划分析 | SQLGlot 做离线候选抽取和差异分析 | SQL、方言、schema → AST、引用、候选血缘/差异 | SQLGlot 官方说明解析较宽松，解析通过不等于引擎可运行；UDF、动态 SQL、模板宏需标 unknown |
| 本体管理 | 内网 Git 中版本化 YAML/JSON/Markdown＋评审单 | 复杂 OWL、协同编辑、推理需要时评估 Protégé/WebProtégé 或内部方案 | 业务证据 → 概念、关系、约束及版本 | Protégé 支持 OWL 编辑与推理，不能自动批准业务含义；托管 WebProtégé 不应用于未批准外发的企业知识 |
| 语义表达 | 复用 Dataphin/内部指标定义与批准 SQL；用本指南模板补齐缺失契约 | 有交换或跨引擎需求时评估 Apache Ossie；已采用 dbt 时评估 [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow) | 指标定义＋资产 → 可计算语义与来源 | Ossie 基线是开发草案，需单独核验校验器、SDK、转换器和目标引擎；MetricFlow 适合已有 dbt 体系，不为使用工具而平移平台 |
| 约束检查 | Git 评审、JSON Schema/自定义检查、现有质量规则 | 已采用 RDF 图且需要图约束时用 SHACL | 定义/图＋约束 → 诊断和报告 | W3C SHACL 验证 RDF 图；不能验证指标业务正确或替代人工审批 |
| 检索 | 结构化筛选（域、类型、状态、版本、权限）＋关键词 | 人工金标显示召回不足后，加内网向量检索与重排 | 任务上下文 → 可见定义/资产和来源 | embedding 不存放指标真值；权限必须在召回与返回两端生效 |
| Agent 工具 | 先直接调用少量内部 API/函数工具 | 客户端多、工具复用需求明确时封装内网 MCP | 类型化参数 → 状态、证据、覆盖范围 | MCP 标准化工具发现和调用，但不自动获得权限、质量或审计；身份在服务端验证 |
| 轨迹与评估 | 现有日志/监控平台＋任务评审表 | 需要 Agent 专项追踪并获准部署时评估[自托管 Langfuse](https://langfuse.com/self-hosting) 等 | 任务、工具调用、结果、评分 → 回归与错误分类 | 公司内容留内网；日志最小化。官方提供自托管方式，但生产运维、许可功能和数据策略需自行承担 |

## MaxCompute＋Dataphin 的最小接法

1. 让 Dataphin/平台管理员确认：公司版本、资产搜索和血缘 API、RAM/内部身份方式、字段级信息、分页、流控和审计。公开的 [`GetTableLineageByTaskId`](https://api.aliyun.com/document/dataphin-public/2023-06-30/GetTableLineageByTaskId) 证明 Dataphin Public API 中存在表血缘查询并需要 RAM 授权，但不能据此假定公司实例可调用。
2. 建一个只读适配层，只暴露试点产品相关资产；内部对象使用平台稳定 ID。适配层把平台状态转换为 [架构文档定义的统一状态](architecture.md#建议工具契约)，保留 source_version、observed_at 和 coverage。
3. 批准 SQL 保留在现有开发/发布体系中。首期 Agent 获取 SQL 引用和经过脱敏的逻辑摘要；是否返回完整 SQL由公司权限决定。
4. MaxCompute 查询首期不开放给模型。需要计划诊断时，可对批准 SQL 通过受控工具调用 [EXPLAIN](https://help.aliyun.com/zh/maxcompute/explain-1)；官方文档说明它输出 Job、Task 和 Operator 依赖，也提示过大输出可能被 API 限制。EXPLAIN 不执行结果验证。
5. 后续确需查询时，仅开放批准指标或参数化查询，使用独立只读身份、分区必填、超时、费用/扫描量、返回量和审计控制；[MaxCompute 权限](https://help.aliyun.com/zh/maxcompute/user-guide/maxcompute-permissions)应按现有项目、表、敏感数据及相关对象管理。

## SQLGlot 的角色

[SQLGlot](https://sqlglot.com/) 可解析 SQL AST、遍历表达式并提供 [lineage API](https://sqlglot.com/sqlglot/lineage.html)，适合自动生成“表/字段引用、聚合、过滤、关联条件、两个 SQL 的结构差异”等候选。必须显式传入尽可能匹配的方言，并用真实 MaxCompute SQL 样本评估解析覆盖率。

建议输出四种状态：parsed、partial、unsupported、failed；后两者转人工。不要因为解析器返回 AST 就自动更新生产血缘，也不要把两段结构相似 SQL 判为业务等价。

## 本体与语义工具怎么选

- 首期：Git＋模板＋review owners。优势是低门槛、可 diff、能和 SQL/任务版本一起评审；不足是交互编辑和推理较弱。
- [Protégé/WebProtégé](https://protege.stanford.edu/software/)：在明确采用 OWL、需要类层次、逻辑公理、推理或多人本体编辑时评估。企业部署和权限先审查，不把内网知识上传到未批准服务。
- Ossie：在需要将逻辑语义和本体映射以开放格式交换时评估；本地固定版本校验可用于结构和引用检查，但这不构成 MaxCompute 执行器。
- [SHACL](https://www.w3.org/TR/shacl/)：已有 RDF 数据图且需要检查形状约束时使用；业务规则和指标结果仍需其他验证。

## 直接 API、函数工具与 MCP

首期工具少且只有一个 Agent 客户端时，直接函数/API 适配最省维护；每个接口有固定 schema、超时、错误状态和审计即可。MCP 的价值是让多个兼容客户端发现和调用统一工具。[MCP 工具规范](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)明确工具由模型发现调用，并建议保留可拒绝调用的人类控制；认证和授权仍由部署方落实。

无论使用哪种协议，必须做到：服务端身份、最小权限、参数白名单、输出裁剪、来源版本、工具级审计、写操作单独审批。协议选择不会修复错误血缘或模糊指标。

## 最小工具集和扩展顺序

第一阶段只做 `search_assets`、`get_asset`、`get_lineage`、`get_definition`、`get_mapping`、`get_approved_sql` 和 `compare_definitions`，足够支撑口径定位助手。第二阶段为规则变更增加影响图遍历和评审任务接口。第三阶段为研发辅助增加代码/作业检查、分支工件和发布前验证；写入、发布、调度操作继续由现有平台和人工审批控制。

## 采用前检查

- 真实内网环境是否允许安装、服务部署和模型访问？数据能否离开公司网络？
- 平台接口是否覆盖试点需要的资产、血缘、负责人和版本？调用身份如何继承用户权限？
- 工具返回能否区分无权限、无数据、超时、截断和过期？
- 哪些定义有业务 owner，哪些 SQL 已批准，谁能处理冲突？
- 维护一条映射和一次模型变更的成本是多少？是否由实际任务持续消费？
