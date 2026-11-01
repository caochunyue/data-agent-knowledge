# 数据 Agent 知识库与落地实践

研究截止：2026-11-01。私有研究库；中文原创总结和可复现实验。

**当前状态：已登记用户截图中的 36 个账号并逐个执行首轮公开检索，6 篇公开版本已读相关章节；微信原文阅读仍为 0，未完成一年历史覆盖。官方研究、最小案例和回归评测已建立。**

## 阅读入口

1. [面向数据研发的 Agent 落地指南](docs/practice/README.md)：架构、双向建模方法、模板、工具、三个应用案例和试点清单；[Ossie 专题区](docs/ossie/README.md)单独标识语义模型与本体映射内容。
2. [MaxCompute＋Dataphin 离线研发实践包](docs/offline-rd/README.md)：中间层、应用层、链路优化、平台适配与价值评测。
3. [关注账号文章发现](docs/followed-account-findings.md)、[全年采集规程](docs/collection/README.md)与[来源状态](sources/README.md)。
4. [业界进展判断](docs/industry-report.md)与[推荐架构](docs/architecture.md)。
5. [知识库与 Harness](docs/topics/knowledge-and-harness.md)、[OSI / Ossie](docs/topics/osi-semantic-model.md)、[本体实践](docs/topics/ontology-practice.md)、[评测体系](docs/topics/evaluation.md)。
6. 分类：[数据研发](docs/categories/数据研发.md)、[资产检索答疑](docs/categories/资产检索答疑.md)、[数据分析](docs/categories/数据分析.md)、[数据 Agent](docs/categories/数据agent.md)。
7. [案例说明](examples/README.md)、[验收报告](reports/acceptance.md)、[实施记录](docs/implementation-ledger.md)。

## 运行（基础案例只需 Python 3.9+ 标准库）

```bash
python3 -m unittest discover -s tests -v
python3 examples/lab.py
python3 examples/lab.py '{"tool":"search","query":"客户"}'
python3 scripts/evaluate.py
python3 scripts/validate_index.py
python3 scripts/audit_coverage.py --accounts sources/collection-accounts.json --articles sources/collection-articles.json --output reports/collection-coverage.json
```

Ossie 格式校验是可选步骤：按 examples/README.md 安装固定依赖后执行；它不影响标准库案例运行。评测输出保存在 reports，不调用云 API、不需要模型凭据。

## 能力边界

案例是**确定性工具 Harness 基线**，接受结构化 JSON 动作，不是能理解任意自然语言的 LLM Agent。40 条用例是开发回归集，四类各 10 条；不代表泛化能力或生产水位。检索使用明确同义词精确匹配；语义查询使用固定指标模板；本体使用复合身份和已批准关系；没有通用 Ossie 查询编译器。

建议先运行案例观察错误关联和正确关联的差异，再学习专题中的生产扩展。公众号采集恢复后，以来源规程增量整理；没有创建定时任务。

## 版权与资料

原创文档仅含总结、链接和必要短引文；不保存未授权公众号全文。examples/schemas 为固定版本 Apache Ossie schema，许可证和 NOTICE 随附。案例中的客户、订单、邮箱全部合成，非真实用户资料。
