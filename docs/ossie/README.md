# Ossie 专题区

此目录用于标识和集中入口管理 Apache Ossie / OSI 语义模型、本体模型与映射相关内容。

## 内容边界

- Apache Ossie Core Spec、Ontology、Mapping 及其版本核验。
- 业务本体、计算语义、资产映射之间的关系。
- Ossie 在数据研发 Agent、指标口径和数据资产治理中的应用边界。
- 规范、校验器、SDK、转换器和目标执行引擎的能力区分。

## 推荐阅读路径

按“先理解规范，再构建本体，随后桥接资产，最后接入 Agent”的顺序阅读。只想开始试点时，可直接从第 3 类和第 4 类开始。

### 1. 规范基础：Ossie 描述什么

- [规范深读：Core、Ontology 与 Mapping](spec-deep-dive.md)
- [Ossie / OSI 语义模型说明](../practice/modeling-playbook.md#ossie-能帮到哪里)
- [固定版本来源索引](../../sources/practice-references.json)

### 2. 本体构建：从业务材料抽取概念

- [从资产语义模型构建业务本体：落地手册](ontology-bridge-playbook.md)
- [双向建模操作手册](../practice/modeling-playbook.md)
- [业务本体、语义、映射与 SOP 模板](../practice/templates.md#4-业务本体卡)

### 3. 桥接映射：从本体落到资产语义

- [贯穿样板：资产语义模型到业务本体与 Mapping](asset-to-ontology-example.md)
- [桥接到数据研发 Agent 的方法](bridge-and-agent.md)
- [跨模板贯穿示例](../practice/worked-example.md)
- [业务本体、语义、映射与 SOP 模板](../practice/templates.md#6-融合映射卡)

### 4. Agent 应用：把模型用于真实任务

- [数据研发 Agent 落地指南总入口](../practice/README.md)
- [七层架构与工具契约](../practice/architecture.md)
- [三个 Agent 应用案例](../practice/agent-cases.md)
- [真实工作试点清单](../practice/pilot.md)

### 5. 工具、验证与治理

- [工具与接法](../practice/tools.md)
- [业务本体、语义、映射与 SOP 模板](../practice/templates.md#10-评审时必问的问题)
- [专题验收记录](../../reports/practice-guide-review.md)

通过本页可以找到知识库内当前已沉淀的 Ossie 相关专题内容；来源索引再指向 Apache Ossie 官方规范和校验器。公众号文章原文及其采集记录仍属于公众号资料区，不会伪装成 Ossie 专题知识。

当前采用“目录标识＋完整索引”的方式，暂不移动既有文件；这样可以保持 README、原聊天和其他专题已有链接稳定。后续新增 Ossie 文档必须同步登记到本页。

## 版本基线

当前 Apache Ossie 基线：`48da55a07e4e8c3a11a662b14727557f6342536d`。

本目录不放企业真实表名、SQL、用户标识或未授权业务资料。
