# 知识文档层

`docs/` 是人读知识层：解释证据、规范、方法和场景，不保存运行结果，也不替代 `sources/` 的事实账本。

## 五个知识面

| 子域 | 回答的问题 | 入口 |
|---|---|---|
| 微信渠道 | 文章实际说了什么、证据到什么程度 | [wechat/](wechat/README.md) |
| OSI/Ossie | 规范如何表达计算语义、本体和映射 | [ossie/](ossie/README.md) |
| 跨域专题 | Harness、评测、本体实践等共性原理 | [topics/](topics/README.md) |
| 通用落地方法 | 如何从业务问题构建 Agent 工件 | [practice/](practice/README.md) |
| 离线研发场景 | MaxCompute＋Dataphin 如何落地 | [offline-rd/](offline-rd/README.md) |

## 治理与视图

- [bridge/](bridge/README.md)：只描述来源知识如何进入语义、工具、评测和工程决策。
- [collection/](collection/README.md)：微信采集、阅读状态和覆盖闭合规则。
- [categories/](categories/README.md)：按四类场景查看微信知识卡，不是原始来源。
- [架构总图](architecture.md)、[行业报告](industry-report.md)、[实施决策记录](implementation-ledger.md)：跨域治理页。
- [关注账号发现](followed-account-findings.md)：历史检索发现，不能替代正式文章账本。

## 阅读顺序

1. 想判断证据：先读 `wechat/` 或 `sources/README.md`。
2. 想学习语义/本体：读 `ossie/`，再读 `topics/`。
3. 想在工作中落地：读 `offline-rd/`，然后使用 `templates/`，最后在 `examples/` 和 `evals/` 验证机制。
4. 想评估是否真的可用：读 `reports/README.md`，区分确定性回归、来源校验和企业待验证项。

## 不能混淆的边界

- 微信文章是经验来源，Ossie 是规范来源；两者互不证明。
- `topics/` 和 `practice/` 是原创综合方法，必须注明所依赖的来源证据。
- `examples/` 是合成教学机制，不是 MaxCompute、Dataphin 或企业生产环境证明。
