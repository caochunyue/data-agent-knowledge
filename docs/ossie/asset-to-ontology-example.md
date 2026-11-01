# 贯穿样板：从资产语义模型到业务本体与 Ossie Mapping

本文是可照着执行的脱敏样板。字段、产品和规则均为设计示例，不代表任何真实系统。它展示的重点是推导顺序和审计工件。

## 1. 输入：已有资产语义模型

假设团队已经批准以下逻辑数据集：

| dataset | 一行代表什么 | 完整身份 | 关键字段 |
|---|---|---|---|
| `redemption_instances` | 一次成功或失败的权益领取实例 | `tenant_id + product_id + instance_id` | `user_id`、`plan_id`、`rule_version`、有效期 |
| `redemption_transactions` | 一次核销尝试及其终态 | `tenant_id + transaction_id` | `instance_id`、结果、交易时间、冲正标记 |
| `users` | 一个主体在租户范围内的身份 | `tenant_id + user_id` | 主体类型、状态 |
| `plans` | 一个权益方案版本 | `tenant_id + plan_id + version` | 方案类型、有效期规则 |

已有 semantic model 还定义了 `redemption_instances → users`、`redemption_transactions → redemption_instances` 等逻辑连接，以及“批次实例核销率”的批准分子、分母和观察时点。

## 2. 从字段抽取候选本体

先建立候选表，保留来源和未决问题，不直接批准：

| 候选概念 | 类型 | 来源 | 需要确认 |
|---|---|---|---|
| 领取实例 | EntityType | `redemption_instances` | 实例号是否跨产品重用；规则版本是否入身份 |
| 核销交易 | EntityType/Event | `redemption_transactions` | 请求、成功、冲正是否是不同事实 |
| 用户 | EntityType | `users` | 主体合并、注销、匿名范围 |
| 权益方案 | EntityType | `plans` | 版本是属性还是独立对象 |
| 交易结果 | ValueType | `result_code` | 哪些值属于最终成功 |
| 有效期 | ValueType | `valid_from/valid_to` | 时区和 as-of 规则 |

抽取可自动化的部分包括字段、SQL AST、血缘、候选主键和同名术语；实体边界、关系含义、成功终态、身份范围和指标分母必须人工批准。

## 3. 业务本体 v0.1 的设计

### 概念和身份

```yaml
ontology: RedemptionDomain
concepts:
  - concept: RedemptionInstance
    type: EntityType
    identify_by: [tenant, product, instance_id]
  - concept: RedemptionTransaction
    type: EntityType
    identify_by: [tenant, transaction_id]
  - concept: User
    type: EntityType
    identify_by: [tenant, user_id]
  - concept: BenefitPlan
    type: EntityType
    identify_by: [tenant, plan_id, version]
  - concept: ResultCode
    type: ValueType
```

这里没有把一张表直接等同于一个实体：`RedemptionTransaction` 是否同时代表“核销尝试”和“成功核销事实”，需要由状态终态和冲正规则进一步区分。

### 关系和约束

```yaml
relations:
  - name: held_by
    subject: RedemptionInstance
    object: User
    multiplicity: ManyToOne
    condition: 领取记录已成功生成且主体身份可解析
  - name: belongs_to_plan
    subject: RedemptionInstance
    object: BenefitPlan
    multiplicity: ManyToOne
    condition: 方案版本在领取时有效
  - name: consumes
    subject: RedemptionTransaction
    object: RedemptionInstance
    multiplicity: ManyToOne
    condition: 交易达到批准成功终态且未被冲正
```

必须同时登记反例：失败请求不成立 `consumes`；已冲正交易不计入成功核销；缺少实例 ID、迟到分区或无权限时是 `unknown`，不是“不成立”。

## 4. Mapping 的落地方式

Mapping 文档绑定一个 ontology 版本和一个 semantic model 版本。示意如下：

```yaml
ontology_ref: RedemptionDomain@0.1
semantic_model_ref: RedemptionSemantic@2026-11-01
concept_mappings:
  - concept: RedemptionInstance
    object_mappings:
      - referent_mappings:
          - relationship: tenant
            expression: redemption_instances.tenant_id
          - relationship: product
            expression: redemption_instances.product_id
          - relationship: instance_id
            expression: redemption_instances.instance_id
  - concept: RedemptionTransaction
    object_mappings:
      - referent_mappings:
          - relationship: tenant
            expression: redemption_transactions.tenant_id
          - relationship: transaction_id
            expression: redemption_transactions.transaction_id
    link_mappings:
      - object_mapping: <当前交易对象映射>
        children:
          - relationship: consumes
            object_mapping:
              concept: RedemptionInstance
              referent_mappings:
                - relationship: tenant
                  expression: redemption_transactions.tenant_id
                - relationship: product
                  expression: redemption_transactions.product_id
                - relationship: instance_id
                  expression: redemption_transactions.instance_id
```

实际文件中应使用固定版本的 Ossie 字段结构；上例用占位符表达审计重点：身份必须完整，关系必须由路径和业务条件共同证明，不能只写 `instance_id`。

## 5. 指标如何挂接而不混淆层次

“批次实例核销率”仍属于 semantic model 的 metric：

```yaml
metric: batch_instance_redemption_rate
subject: RedemptionInstance
numerator: 实例存在至少一笔批准成功且未冲正的 consumes 事实
denominator: 该领取批次中已合资格的 RedemptionInstance
time_semantics: as_of observation_time
aggregation: non_additive
ontology_refs: [RedemptionInstance, RedemptionTransaction, consumes]
```

本体说明指标描述哪些业务对象和关系；semantic model 承载可执行表达式、粒度、过滤和聚合。两者不可互相替代。

## 6. 质量门槛与验证工件

发布前至少保留四类结果：

| 检查 | 证明什么 | 不能证明什么 |
|---|---|---|
| Schema 校验 | 文件结构符合 Ossie Schema | 业务关系正确 |
| 引用/表达式校验 | 概念、关系、dataset、field 可解析 | 数据实际满足唯一性 |
| 数据剖面 | 当前快照的唯一性、孤儿、迟到、基数 | 业务定义已获批准 |
| 人工评审 | 概念、关系、例外和指标口径已确认 | 未来资产不会变化 |

首期质量指标建议记录：关键概念覆盖率、完整身份率、关键指标 mapping 覆盖率、无证据关系数、待确认关系数、数据剖面失败数、mapping 失效数。

## 7. Agent 如何消费这套工件

当研发询问“某产品核销率为什么和报表不同”时，Agent 应：

1. 锁定产品、指标、观察时点和批准 bundle 版本。
2. 读取本体，确认实例、交易、方案和 `consumes` 的业务定义。
3. 读取 mapping，定位完整身份、成功条件、冲正排除和资产字段。
4. 通过只读工具检查当前 schema、血缘、分区和质量状态。
5. 按 SOP 比较分子、分母、粒度、时间窗口和去重规则。
6. 输出证据、差异、缺口和待确认项；缺少完整 mapping 时停止猜测。

## 8. 推荐目录与版本

```text
knowledge/
  ontology/common/                 # 稳定公共概念
  ontology/domains/redemption/     # 领域本体
  semantic/domains/redemption/     # Ossie semantic model
  mapping/domains/redemption/      # ontology ↔ semantic mapping
  evidence/domains/redemption/     # 来源和评审记录
  sop/domains/redemption/          # 任务契约
```

本地知识库可先以 Markdown/YAML 和 Git 管理；只有当概念规模、协作人数、查询复杂度或跨系统复用达到阈值，再考虑图数据库、专用本体编辑器或向量索引。所有发布包都应锁定 ontology、semantic、mapping、SOP、证据和评审版本。

