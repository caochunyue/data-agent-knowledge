# 可填写工件层

`templates/` 将知识文档变成可审查工作产物，不包含真实企业数据。

- `offline-rd/requirement-contract.md`：业务需求、口径、范围和验收契约。
- `offline-rd/asset-decision.md`：资产复用、新建与粒度判断。
- `offline-rd/release-and-backfill.md`：发布、回补、幂等和影响检查。
- `offline-rd/optimization-experiment.md`：优化假设、对照、资源条件和回退。

使用顺序：从 `docs/offline-rd/` 选任务 → 填模板 → 用 `examples/` 理解机制 → 用 `evals/`/`reports/` 验证工具边界。模板不是审批本身，真实发布仍需企业流程。
