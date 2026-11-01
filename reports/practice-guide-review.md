# 数据研发 Agent 落地指南验收记录

核验日期：2026-11-01。

## 交付覆盖

- 七层架构、上下文分层、建议工具契约和组件引入条件。
- 数据知识与业务本体双向建模的七步操作手册。
- 证据、资产、本体、指标、映射、SOP、Agent 结果和变更评审模板。
- MaxCompute、Dataphin 环境下的默认接法与工具选择边界。
- 指标口径/资产定位、规则变更影响、新产品数据设计三个 Agent 案例。
- 真实任务试点清单、角色分工及价值/维护成本测量。
- 一个不含数据和代码的跨模板贯穿示例。

没有新增合成数据、实验代码或真实系统接入。小程序对象和规则均标为建议模型，需企业内确认。

## 独立审查

独立只读审查认为架构、方法、安全边界、Ossie 能力分层和三个案例整体符合要求，无 Critical 问题。审查提出的 Important 项已处理：

1. 增加证据卡和权威边界，规定业务定义、生产实现、元数据和数据观察不能静默互相覆盖。
2. 指标模板增加 aggregation_behavior、allowed_rollups、incompatible_dimensions 和 reaggregation_method，并将聚合兼容纳入首期案例。
3. 补齐 DataHub、MetricFlow 和 Langfuse 官方来源及文档链接。

Minor 项已处理：新增跨模板贯穿示例；说明专题参考索引是主张—来源账本，使用独立字段结构。

## 实际检查

| 检查 | 结果 |
|---|---|
| `sources/practice-references.json` JSON 解析、ID 唯一 | 通过；13 条来源 |
| `docs/practice` 必需文档和相对链接 | 通过；8 份文档 |
| `git diff --check` | 通过 |
| `python3 -m unittest discover -s tests -v` | 16/16 通过 |
| 原有确定性行为回归 | 40/40 通过；未评测模型 |
| 全库 `scripts/validate_index.py` | 通过；来源字段、日期、重复 ID/URL 和本地 Markdown 链接无错误 |

验证期间，并发专题一度有 3 个尚未创建的本地链接；该专题完成文件后重新运行，最终检查通过。

## 尚未验证

- 公司 Dataphin/MaxCompute 的实际版本、开放接口、权限和内网模型服务。
- 支付宝/芝麻信用真实业务对象、规则、表和 SQL。
- 三个 Agent 案例的真实完成率、时效与收益；需按试点清单测量。
- Ossie 到 MaxCompute 的执行或转换兼容；本指南只核对固定版本规范和校验代码的能力边界。
