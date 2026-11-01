# 可填写模板：把业务、资产与 SOP 固化为版本化工件

模板中的尖括号均需替换；“未知”必须说明责任人和补齐方式。模板可先放在 Git 管理的 Markdown/YAML 中，企业真实内容只进入批准的内网仓库。

## 1. 任务卡

```yaml
task_id: <稳定 ID>
name: <例如：核销率口径与数据定位>
business_scope: <产品/业务域>
requester_and_decision: <谁用结果做什么>
input_examples: <历史问题或需求单引用>
expected_artifact: <差异单/影响清单/设计清单>
current_process:
  owner: <当前处理人>
  baseline_period: <基线时间范围>
  median_active_minutes: <只统计实际投入>
  handoffs: <交接次数>
  reopen_reason: <返工原因>
acceptance_owner: <验收人>
out_of_scope: <例如：自动发布、任意 SQL>
```

## 2. 证据卡与权威边界

```yaml
evidence_id: <稳定 ID>
evidence_type: <business_definition/implementation/metadata/observation/review>
title: <材料标题>
locator: <内网可定位地址或平台 ID>
authority_scope: <该材料能证明什么>
cannot_prove: <不能由它推出什么>
source_owner: <来源负责人>
source_version: <文档版本/代码提交/资产快照/观察时间>
business_valid_time: <业务有效期；不适用写 n/a>
observed_at: <采集或观察时间>
coverage: <产品、资产、时间及已知缺口>
confidentiality_and_access: <分级和访问范围>
supersedes: [<被替代证据 ID>]
status: <current/stale/disputed/withdrawn>
```

证据按它实际能证明的范围使用，不能静默相互覆盖：

| 证据类型 | 能证明什么 | 冲突时谁裁决 |
|---|---|---|
| 业务定义/评审 | 业务含义、规则、例外和适用范围 | 业务 owner |
| 版本化生产代码/SQL | 指定版本实际实现了什么逻辑 | 数据/系统 owner；不反向批准业务含义 |
| 平台元数据/血缘 | 指定采集时点的结构、依赖和负责人 | 平台/资产 owner；截断范围须保留 |
| 数据观察/质量结果 | 指定快照中观测到的状态 | 数据 owner；不能直接推出业务规则或因果 |
| Agent/自动抽取候选 | 待核验的结构和差异线索 | 相应业务或数据 owner |

定义与实现不一致时同时保留，标为 disputed，并创建评审任务；在 owner 裁决前 Agent 只能报告冲突。新的来源只有明确 `supersedes` 和生效时间后才替代旧证据。

## 3. 数据资产卡

```yaml
asset_id: <平台稳定 ID，不用展示名代替>
asset_type: <table/field/job/report/api/metric>
locator: <内网可定位地址或平台 ID>
display_name: <名称>
grain: <一行代表什么；非表资产写 n/a>
identity: [<联合身份字段>]
time_fields:
  event_time: <字段或 n/a>
  processing_time: <字段或 n/a>
  partition_time: <字段或 n/a>
relationships:
  - target_asset_id: <ID>
    join_or_dependency: <条件>
    expected_cardinality: <1:1/1:N/N:1/N:N>
quality_and_freshness: <完整性、延迟、异常处理>
owner: <负责人/团队>
classification_and_access: <分级和授权方式>
source_version: <平台版本/代码提交/采集时间>
evidence_refs: [<材料 ID>]
status: <candidate/reviewed/approved/deprecated>
```

## 4. 业务本体卡

### 概念/实体

```yaml
concept_id: <命名空间内稳定 ID>
name: <业务名称>
kind: <entity/value/event>
definition: <必要且充分的业务含义>
aliases: [<别名；不表示自动等价>]
identity:
  components: [<完整身份组成>]
  scope: <产品/租户/全局>
  lifecycle: <创建、合并、失效、重用规则>
attributes:
  - name: <属性>
    type_or_unit: <类型/单位>
    semantics: <含义>
states_and_events: <状态维度和触发事件；无则 n/a>
counterexamples: [<容易混淆但不属于本概念的例子>]
owner: <业务负责人>
evidence_refs: [<制度/产品规则/评审材料>]
valid_from: <生效时间>
valid_to: <失效时间或 null>
status: <candidate/reviewed/approved/deprecated>
```

### 关系与约束

```yaml
relation_or_rule_id: <稳定 ID>
subject: <概念 ID>
predicate: <关系/规则名称>
objects_or_roles: [<概念 ID 与角色>]
multiplicity: <基数；未知需列为问题>
condition: <关系或结论成立条件>
exceptions: [<例外>]
unknown_policy: <缺证据/无权限/数据迟到时如何处理>
temporal_scope: <as-of、有效期、事件时间要求>
evidence_refs: [<来源 ID>]
owner: <批准人>
status: <candidate/reviewed/approved/deprecated>
```

## 5. 计算语义/指标卡

```yaml
metric_id: <稳定 ID>
name: <指标名>
business_question: <支持什么决策>
subject_and_grain: <统计对象与输出粒度>
population: <总体与资格>
numerator: <分子；非比率写 n/a>
denominator: <分母；非比率写 n/a>
dimensions: [<允许维度>]
aggregation_behavior: <additive/semi_additive/non_additive/derived>
allowed_rollups: [<可安全汇总的维度和时间粒度>]
incompatible_dimensions: [<禁止或需重算的维度组合>]
reaggregation_method: <从基础分子分母/快照/去重明细重算；不适用写 n/a>
time_semantics:
  event_or_cohort: <发生期/批次追踪/as-of>
  timezone: <时区>
  maturity_window: <成熟窗口或 n/a>
deduplication: <去重身份和规则>
filters_and_exclusions: [<过滤/取消/豁免等>]
null_zero_and_late_data: <空值、零分母、迟到处理>
unit_and_precision: <单位、精度>
approved_sql_ref: <批准 SQL ID 与版本，不在公开库粘贴真实 SQL>
ontology_refs: [<概念/关系/规则 ID>]
owner: <业务口径负责人>
technical_owner: <数据负责人>
status: <candidate/reviewed/approved/deprecated>
```

## 6. 融合映射卡

```yaml
mapping_id: <稳定 ID>
mapping_type: <identity/attribute/fact/rule/metric>
business_ref: <本体或指标 ID + 版本>
asset_refs: [<资产 ID + 版本>]
logical_fields: [<逻辑字段>]
source_fields_or_expression: <字段或批准表达式引用>
evidence_condition: <什么记录和条件足以证明该事实>
complete_identity: [<所有身份组成，不得省略产品/租户范围>]
cardinality_and_join: <基数和关联条件>
time_alignment: <事件、处理、分区及 as-of 对齐>
null_duplicate_late_policy: <异常处理>
coverage_and_gaps: <覆盖产品、时间、缺口>
business_owner: <业务确认>
technical_owner: <数据确认>
valid_from: <生效时间>
valid_to: <失效时间或 null>
status: <candidate/reviewed/approved/deprecated>
test_or_review_refs: [<历史任务/验收记录>]
```

## 7. SOP 任务契约与产品绑定

```yaml
sop_id: <稳定 ID>
name: <任务名称>
version: <版本>
goal: <可验收目标>
applicability:
  product_bindings: [<产品 + 规则版本>]
  task_types: [<适用问题>]
inputs:
  required: [<必需参数>]
  optional: [<可选参数>]
ontology_and_metric_refs: [<批准定义 ID + 版本>]
allowed_tools: [<工具及只读/写入级别>]
steps:
  - id: S1
    action: <人或 Agent 要完成的动作>
    input_refs: [<输入/上一步输出>]
    tool_or_human: <工具名/业务确认/研发确认>
    output: <结构化产物>
    checks: [<进入下一步前的确定性检查>]
    on_failure: <停止、补充、降级或转人工>
completion:
  required_evidence: [<必须引用的证据>]
  acceptance: [<完成条件>]
  forbidden_claims: [<证据不足时不得输出的结论>]
escalation:
  business: <业务冲突/规则未知>
  data: <资产、质量、SQL 问题>
  security: <越权/敏感信息>
owner: <SOP 负责人>
status: <candidate/reviewed/approved/deprecated>
```

产品绑定只允许替换 SOP 声明的参数，如产品 ID、批准规则和指标版本。若事实定义或流程完成条件不同，应新建 SOP 版本或变体并评审。

## 8. Agent 结果工件

```yaml
task_run_id: <运行 ID>
request: <用户问题摘要>
auth_scope: <服务端确认的业务域/工具范围，不记录令牌>
model_bundle: <本体+语义+映射+SOP 版本>
clarifications: [<已确认与未确认问题>]
findings:
  - claim: <结论>
    evidence_refs: [<来源/工具结果 ID>]
    status: <confirmed/candidate/unknown>
tool_calls: [<request_id、工具、状态、覆盖范围>]
gaps_and_warnings: [<缺口、过期、截断>]
recommended_next_actions: [<可执行建议及负责人>]
review:
  reviewer: <角色>
  decision: <accepted/corrected/rejected>
  correction_refs: [<反馈与模型更新 ID>]
```

## 9. 变更评审单

```yaml
change_id: <ID>
change_type: <ontology/metric/mapping/sop/asset>
reason_and_source: <变更依据>
before_after: <语义差异，不只贴文本 diff>
effective_time: <业务生效时间>
affected_products: [<产品>]
affected_definitions_assets_sops: [<影响清单>]
historical_policy: <历史重算/旧版保留/as-of>
regression_tasks: [<需重放的真实历史任务>]
approvals:
  business: <结论/待定>
  data: <结论/待定>
  platform_security: <如需要>
rollback_or_superseded_version: <回退/被替代版本>
```

## 10. 评审时必问的问题

- 概念身份是否完整？同名、跨产品、合并拆分和历史变化如何处理？
- 每个业务事实有什么足够证据？“请求发起”和“最终成功”是否混淆？
- 指标的统计对象、分子分母、时间和去重是否能够被另一位研发复现？
- 指标是可加、半可加还是不可加？按哪些维度能汇总，哪些组合必须从基础事实重算？
- 映射是否保留基数、as-of、迟到和异常规则？缺证据是否被错误当作否定事实？
- SOP 的每一步能否判断完成或失败？产品差异是否显式绑定版本？
- Agent 输出的每个关键主张是否有支持它的证据，而不仅是附带一个 URL？
