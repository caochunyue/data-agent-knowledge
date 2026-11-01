# 贯穿示例：产品 P 的核销率口径差异任务

这是不含数据行和可执行代码的填写示例，展示模板 ID 如何相互引用。产品 P、定义和规则均是假设，不能替代企业内评审。

## 引用链

```text
TASK-REDEEM-DIFF-01
  ├─ EV-BIZ-REDEEM-01（业务定义）
  ├─ EV-SQL-REPORT-A-01（报表 A 实现）
  ├─ CONCEPT-BENEFIT-INSTANCE-V1
  ├─ FACT-SUCCESSFUL-REDEMPTION-V1
  ├─ METRIC-COHORT-REDEMPTION-RATE-V1
  ├─ MAP-REDEMPTION-FACT-V1
  └─ SOP-METRIC-DIFF-V1
```

## 核心卡片摘要

**任务卡** `TASK-REDEEM-DIFF-01`：解释报表 A/B 的定义与数据实现差异；输出证据化差异单，不负责自动修改生产报表。

**证据卡**：

- `EV-BIZ-REDEEM-01` 类型为 business_definition，authority_scope 是产品 P 成功核销和部分核销规则，由业务 owner 批准；它不能证明生产 SQL 已实现该定义。
- `EV-SQL-REPORT-A-01` 类型为 implementation，固定代码提交和发布时间，证明报表 A 的实现；它不能反向批准业务口径。
- `EV-META-REDEEM-01` 类型为 metadata，记录资产 schema、血缘采集时间和覆盖深度；截断的血缘不表示没有其他下游。

如果 `EV-BIZ-REDEEM-01` 与 `EV-SQL-REPORT-A-01` 不一致，状态设为 disputed。Agent 输出冲突和负责人，不自行选择一个作为“正确答案”。

**本体卡**：

- `CONCEPT-BENEFIT-INSTANCE-V1` 是领取实例，身份组成和适用产品范围待公司数据契约确认。
- `FACT-SUCCESSFUL-REDEMPTION-V1` 表示核销交易对领取实例产生批准的成功核销事实；请求埋点不能单独作为证据，冲正处理由业务规则确定。

**指标卡** `METRIC-COHORT-REDEMPTION-RATE-V1`：统计对象是领取实例；按领取批次追踪，截至观察日计算。它是 non_additive，渠道和日期层的比率不能直接相加或平均；跨维度汇总需从批准的实例级分子和分母重算。零分母返回不可计算。

**映射卡** `MAP-REDEMPTION-FACT-V1`：将成功核销事实绑定到权威交易资产、成功终态和冲正规则；保留实例完整身份、交易身份、事件时间、数据迟到和映射版本。具体字段和资产 ID 仅在内网填写。

**SOP** `SOP-METRIC-DIFF-V1`：读取任务范围 → 加载 approved 定义 → 获取两指标卡和 SQL 引用 → 比较粒度、时间、去重、聚合及过滤 → 检查资产版本和新鲜度 → 输出 confirmed/candidate/unknown 差异 → 分派业务或数据 owner。

## 预期 Agent 工件

```yaml
task_run_id: RUN-EXAMPLE-01
model_bundle: <固定本体、语义、映射和 SOP 版本>
findings:
  - claim: 报表 A 与 B 使用不同统计对象
    evidence_refs: [<两份批准指标定义>]
    status: confirmed
  - claim: 部分核销处理不同导致数值差额
    evidence_refs: []
    status: unknown
gaps_and_warnings:
  - <部分核销规则或 SQL 分支尚未得到 owner 确认>
recommended_next_actions:
  - <业务 owner 裁决定义；数据 owner 核对实现>
```

这个示例的验收重点是引用链和停止条件，不是生成一段听起来合理的解释。只有拿到相同统计期的授权结果或已有差异分析证据后，才可以解释数值差额。
