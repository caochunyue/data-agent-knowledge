# OSI / Apache Ossie：从规范到可执行口径

## 研究基线

[官方仓库](https://github.com/apache/ossie)当前 README 说明 Ossie 原名 Open Semantic Interchange (OSI)。本轮通过 GitHub API 核验 main 提交 `48da55a07e4e8c3a11a662b14727557f6342536d`（2026-11-01T09:35:19Z），与本地副本一致。以下规范结论固定到该提交；它是 `0.2.0.dev0` 开发草案，不是已发布稳定协议。

[Core Spec](https://github.com/apache/ossie/blob/48da55a07e4e8c3a11a662b14727557f6342536d/core-spec/spec.md)、[本体规范](https://github.com/apache/ossie/blob/48da55a07e4e8c3a11a662b14727557f6342536d/ontology/ontology.md)、[映射 Schema](https://github.com/apache/ossie/blob/48da55a07e4e8c3a11a662b14727557f6342536d/ontology/mapping.json)是主要证据。版本化 schema 快照保留在 examples/schemas，Apache LICENSE/NOTICE 一并保存。

## 四层不要混淆

| 层 | 回答的问题 | 订单案例 |
|---|---|---|
| 物理数据 | 数据存在哪里、什么粒度 | SQLite orders，每个租户内订单唯一 |
| 语义模型 | 逻辑字段、可连接关系、可计算指标是什么 | 已支付金额的条件聚合、订单到客户复合关联 |
| 业务本体 | 哪些业务对象和事实具有稳定含义 | Customer、Order、placed_by |
| 映射 | 数据如何构成对象身份和业务事实 | tenant_id + customer_id 定位 Customer |

同一个字段可能是物理列、逻辑字段或身份的一部分；必须标清语境。Core relationship 表达连接规则，业务本体关系表达命题。能 JOIN 不证明“下单”“付款”“受益人”中哪种关系成立。

## 核心规范落地要点

- 一个独立语义模型包含 version、name 和非空 datasets。dataset 的 primary_key 引用它声明的逻辑字段。
- dataset 内指标表达式使用本 dataset 字段名，模型级指标使用 dataset.field。不能把 source 的原始列名直接混进逻辑引用。
- 表达式可有可移植 SQL 或带 dialect 的实现。规范声明外部方言不意味着工具能查询它；编译适配器必须明确支持范围。
- ai_context 可承载描述和同义词，但不是权限机制；结构与 SQL 仍要校验。
- JSON Schema 校验只证明形状和类型，不能证明指标正确、身份唯一、没有关联放大，也不能证明厂商间执行结果一致。

## 本例如何使用

`commerce.semantic.json` 是固定草案格式的声明示例，`commerce.ontology.json` 定义复合身份，`commerce.mapping.json` 用 referent_mappings 表示身份定位。工具层实际读取 `model.json` 和执行受控 SQLite 模板；**本例没有实现通用 Ossie 编译器或本体查询引擎**。两种文件分开，是为了使教学定义与已实现运行能力清楚可见。

已支付销售额是 paid 订单的 amount_cents 之和：37000 分（370 元），币种 CNY。取消和待支付不纳入，退款未建模，因此不能称净收入或会计收入。若业务说“GMV”，先明确下单/支付、退款、税费、币种、时区和时间归属，再批准一个独立指标，不能套用同义词自动等价。

## 新映射格式与兼容性

固定版本引入独立 mapping 文档，用 ontology_ref、semantic_model_ref 和 concept_mappings 关联两个文档；名字必须与目标文档一致。旧的 ontology_mappings 内嵌形式仍被接受但已弃用。规范明确指出独立文档的 parser/converter 支持另行提供，不能由 schema 存在推断 SDK 已完整支持。

复合身份使用 referent_mappings；对象生成与关系生成分别对应 object_mappings、link_mappings。规范中声明的 relationship 路径要能回到已批准业务对象。本例 validation 脚本离线加载固定 schema，不请求 main 上的漂移引用。

## 接入实际平台的建议步骤

1. 从一条财务认可的指标及其 10–20 个业务问句开始，冻结快照和正确结果。
2. 梳理逻辑字段、类型、粒度、join 基数、时间与过滤条件；先消除双重事实表连接放大。
3. 输出 Ossie 文档，做 schema 与引用检查；明确运行平台支持的表达式和关系子集。
4. 编译/转换到目标平台后，对照手写 SQL 执行结果；跨平台测试 NULL、Decimal、时区、重复行、空集合和除零。
5. 只有迁移前后结果、权限和性能均满足验收，再让 Agent 通过指标工具调用。

当前 [MetricFlow 官方文档](https://docs.getdbt.com/docs/build/about-metricflow)列出 Ossie 文档支持，是可调查的实际接入方向；本轮未部署 dbt，也未验证该转换路径。转换器能生成文件和真正的语义等价要分别验收。
