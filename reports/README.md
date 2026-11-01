# 报告与验收输出层

`reports/` 保存运行后输出和人工验收结论；它们是证据快照，不是新的知识来源。

| 报告 | 生成者/性质 | 说明 |
|---|---|---|
| `evaluation.json`、`traces.json` | `scripts/evaluate.py` | 合成案例的确定性回归和可回放轨迹 |
| `index-validation.json` | `scripts/validate_index.py` | 来源字段、日期、分类、重复与本地链接检查 |
| `collection-coverage.*` | `scripts/audit_coverage.py` | 文章目录覆盖审计；未闭合不等于零篇 |
| `ossie-validation.json` | `scripts/validate_ossie.py` | 固定版本 Schema 格式校验，不证明运行时等价 |
| `acceptance.md` 等 Markdown | 人工验收/专题审查 | 必须区分已实现、已验证、待验证 |

报告引用的输入在 `sources/`、`examples/`、`evals/`；不要手改 JSON 来伪造测试通过。`traces.json` 可能包含本地运行产生的未提交更新，提交前需确认变更来源。
