# 自动化脚本层

脚本把输入账本、案例和金标变成可复查的报告；它们不抓取微信私有数据，也不调用企业生产系统。

| 脚本 | 输入 | 输出 |
|---|---|---|
| `import_articles.py` | 用户批准导入的文章元数据 | 去重后的文章账本 |
| `audit_coverage.py` | 账号与文章账本 | 覆盖 JSON/Markdown 报告 |
| `validate_index.py` | 来源与文档索引 | `reports/index-validation.json` |
| `validate_ossie.py` | 固定 Schema 与示例 | `reports/ossie-validation.json` |
| `evaluate.py` | `evals/cases.json` 与 `examples/` | `reports/evaluation.json`、`reports/traces.json` |

运行方式见根 README。脚本成功只说明其检查范围通过，不能证明公众号全文阅读、企业权限或生产部署。
