# Ossie 规范深读：四种文档各自解决什么

本文按 Apache Ossie 固定基线 `48da55a07e4e8c3a11a662b14727557f6342536d` 解释，不把本地扩展或推测写成规范能力。

## 1. Core Semantic Model：可分析的逻辑契约

Core Spec 的 `semantic_model` 是一个分析领域的逻辑包，不是物理表的复制品。它把“数据在哪里、每行代表什么、如何连接、如何计算”固定下来：

| 对象 | 研发时应回答的问题 | 关键检查 |
|---|---|---|
| `dataset` | 一行是什么、来源是什么、怎样唯一定位 | `source`、`primary_key`/`unique_keys`、粒度 |
| `field` | 属性叫什么、类型是什么、来自列还是表达式 | 名称、类型、表达式方言、时间角色 |
| `relationship` | 哪两个数据集按哪些列连接 | 两端引用、列数相等、基数与过滤条件 |
| `metric` | 指标公式和作用范围是什么 | 分子/分母、聚合、scope、时间过滤 |
| `ai_context` | Agent 如何理解术语、同义词和限制 | 仅辅助理解，不替代批准定义 |
| `custom_extensions` | 目标平台特有的信息如何保留 | 命名空间、版本、损失报告 |

因此 `dataset` 不是“业务实体”，`metric` 也不是本体关系。它们是查询和跨平台交换所需的计算语义。

## 2. Ontology：业务世界的概念契约

Ontology Spec 描述现实对象及其业务语义：

- `EntityType` 是需要通过其他信息再次引用的对象；`ValueType` 是带业务含义的数据类型。
- `extends` 表达概念继承；关系包含角色、方向和 multiplicity。
- `identify_by` 指定哪些关系共同构成对象的首选身份。订单行可能由“所属订单 + 行号”识别，不能只看一个列名。
- `requires`、`derived_by`、`verbalizes` 可表达约束、派生和自然语言说明，但不等于生产规则引擎、审批流或数据质量平台。

本体的粒度比表更稳定：一张宽表可能承载多个概念，一个概念也可能由多个数据集共同证明。

## 3. Mapping：把概念落到逻辑模型

一个独立 mapping 文档绑定一个 ontology 和一个 semantic model。其核心不是给 dataset 加标签，而是回答“哪组表达式产生这个对象或关系”：

1. `concept_mappings` 选择本体概念。
2. `object_mappings` 用 `dataset.field` 或 SQL expression 填充概念属性。
3. `referent_mappings` 沿 `identify_by` 关系递归找到另一个实体，适合复合身份和跨表引用。
4. `link_mappings` 填充概念之间的业务关系，必须说明连接路径，而不是只凭外键猜关系。

桥接时保留完整身份元组（租户、产品、业务 ID、版本、有效期等），并为每条映射记录证据、负责人、适用时间和异常处理。外键只能证明可连接，不能独立证明业务含义。

## 4. 一个最小的桥接思路

以“领取实例由用户持有”为例：

```text
Ontology: 领取实例 --held_by--> 用户
Semantic: redemptions(instance_id, product_id, user_id, status, event_time)
Mapping:
  领取实例.identity <- (product_id, instance_id)
  领取实例.status   <- status 的批准归一规则
  held_by           <- user_id 通过用户 identify_by 解析
```

如果 `user_id` 在不同产品或租户内可重用，就必须把作用域加入身份；如果成功状态还要排除冲正，则把条件写进 mapping 证据或指标实现，而不是让 Agent 自行猜。

## 5. 能力边界

静态校验可检查 JSON Schema、名称与引用、关系列数、SQL 语法、Ontology 的概念/角色/`identify_by`，以及 mapping 对 ontology 和 semantic model 的交叉引用。它不能替代：

- 真实数据中的唯一性、迟到、孤儿、基数和质量验证；
- 指标业务批准、权限控制、SOP 状态推进；
- 查询优化、SQL 执行、结果正确性和生产发布。

固定版本的 ontology 文档对独立 mapping 的 parser/converter 支持仍有兼容性提示；同版 `validation/validate.py` 已包含 mapping/ontology 检查。因此必须分别报告“schema 通过、静态引用通过、数据验证通过、实际执行通过”，不能合并成一个“已支持”。

