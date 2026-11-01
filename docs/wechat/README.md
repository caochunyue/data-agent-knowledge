# 微信渠道知识域

本目录只回答一个问题：**公众号文章实际说了什么，以及哪些内容已被证据核验？**

它不定义 OSI/Ossie 规范，也不把公开研究或本体设计当成公众号原文。

## 分层

1. **来源层**：账号、文章标题、日期、原文链接、阅读状态、访问缺口。权威入口是 [`sources/wechat-observations.json`](../../sources/wechat-observations.json) 和 [`sources/wechat-coverage.json`](../../sources/wechat-coverage.json)。
2. **证据层**：微信窗口逐篇核验、公开渠道补充、局部读取与完整读取的区别。`read_local_window_no_url` 只表示窗口中读到内容，不等于已取得原文 URL；局部读取不得升级为全文结论。
3. **主题层**：按数据研发、资产检索答疑、数据分析、数据 Agent 四类归档；一篇文章可有多个标签，但只能有一个主类。
4. **行动层**：把已核验观点翻译成 MaxCompute＋Dataphin 的任务、SOP、工具接法和验收项；行动建议必须保留来源 ID。

## 当前边界

- “与数据同行”目前只有 13 篇窗口正文记录，最近半年目录没有闭合，不能声称无遗漏。
- 公众号窗口记录与公开搜索记录分开；公开搜索不能证明微信文章已读。
- 本目录不保存未经授权的公众号全文，只保留原创总结、来源链接和必要短引文。

## 阅读顺序

先看 [文章证据索引](articles.md)，再看 [主题地图](topic-map.md)，最后看 [面向 MaxCompute＋Dataphin 的落地转译](translation-to-offline-rd.md)。需要学习 OSI/Ossie 时离开本域，进入 [`docs/ossie/README.md`](../ossie/README.md)。
