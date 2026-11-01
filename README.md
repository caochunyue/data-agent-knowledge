# 数据 Agent 知识库与落地实践

研究截止：2026-11-01。私有研究库；中文原创总结和可复现实验。

**当前状态：已登记用户截图中的 36 个账号并逐个执行首轮公开检索；已在微信窗口核验“与数据同行”13篇正文，并另核验1篇“BAT大数据架构”正文；仍未完成目标公众号最近半年历史目录闭合。官方研究、最小案例和回归评测已建立。**

## 仓库总图

```text
sources/   输入证据与账本        docs/       人读知识与方法
templates/ 任务工件模板          examples/   合成可运行机制
evals/     金标与行为合同        scripts/    导入、校验与评测执行器
tests/     回归保护              reports/    验收与运行输出
```

每个顶层目录都有自己的 README。推荐从 [docs 总入口](docs/README.md) 理解知识，再用 [sources 总入口](sources/README.md) 回查证据，最后查看 [reports 总入口](reports/README.md) 判断哪些能力真正通过了检查。

## 知识库总图

本库现在明确拆成三个入口，避免“来源文章、规范学习、工程落地”混在一起：

1. [微信渠道知识域](docs/wechat/README.md)：公众号文章证据、阅读状态、主题地图和工程转译。
2. [OSI/Ossie 规范知识域](docs/ossie/README.md)：Core Semantic Model、本体、Mapping、版本和验证边界。
3. [知识域桥接层](docs/bridge/README.md)：只记录从文章观点到语义/本体/工具/评测的映射，不充当任何一方的原文。

## 阅读入口

1. [面向数据研发的 Agent 落地指南](docs/practice/README.md)：架构、双向建模方法、模板、工具、三个应用案例和试点清单；[Ossie 专题区](docs/ossie/README.md)单独标识语义模型与本体映射内容。
2. [MaxCompute＋Dataphin 离线研发实践包](docs/offline-rd/README.md)：中间层、应用层、链路优化、平台适配与价值评测。
3. [微信文章证据索引](docs/wechat/articles.md)、[主题地图](docs/wechat/topic-map.md)、[关注账号文章发现](docs/followed-account-findings.md)、[采集规程](docs/collection/README.md)与[来源状态](sources/README.md)。
4. [业界进展判断](docs/industry-report.md)与[推荐架构](docs/architecture.md)。
5. [知识库与 Harness](docs/topics/knowledge-and-harness.md)、[OSI / Ossie](docs/topics/osi-semantic-model.md)、[本体实践](docs/topics/ontology-practice.md)、[评测体系](docs/topics/evaluation.md)。这些是跨域专题，不替代微信或 Ossie 两个来源域。
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
