# Dataphin / MaxCompute 平台适配

## 能力分级

| 能力 | 官方公开依据 | 企业内要核验 | 降级路径 |
|---|---|---|---|
| SQL 保存、预编译、运行、提交 | [SQL 代码任务](https://help.aliyun.com/zh/dataphin/semimanaged-v4/user-guide/computing-tasks/) | 版本、任务类型、权限、研发模式 | 人工在 Dataphin 操作并回填证据 |
| 提交/发布状态机 | [发布管理](https://help.aliyun.com/zh/dataphin/semimanaged-v4/user-guide/release-management-standalone-deployment) | Basic 或 Dev-Prod、审批、对象选择 | 只生成发布清单 |
| 实例/日志/下游读取 | [SDK 1.0 API 参考](https://help.aliyun.com/zh/dataphin/semimanaged-v4/user-guide/untitled-document-49) | OpenAPI 模块、SDK 版本、Endpoint、最小权限 | 已批准导出或人工摘录非敏感结果 |
| OpenAPI 接入 | [OpenAPI 使用](https://help.aliyun.com/zh/dataphin/semimanaged-v4/user-guide/dataphin-openapi-using-documents) | 是否购买、SDK1/2、网络与凭据托管 | 不接入；保留人工门 |
| EXPLAIN | [MaxCompute EXPLAIN](https://help.aliyun.com/zh/maxcompute/explain-1) | 可用命令/SDK、输出上限、配额 | Dataphin 控制台人工执行 |
| 作业诊断 | [Job Insights](https://help.aliyun.com/zh/maxcompute/user-guide/job-insights) | 地域、历史留存、费用口径 | 运行记录与日志人工分析 |

公开 FAQ 曾说明“不提供 API 创建离线任务状态监控”，而 API 参考列有读取实例/日志的接口；两者粒度不同，不能据此宣称可创建完整监控产品。以企业合同、版本和实测为准：[FAQ](https://help.aliyun.com/zh/document_detail/715586.html)。

## 适配器契约

每个适配器声明：操作名、读写级别、参数 schema、平台版本范围、调用主体、超时、分页、扫描/资源预算、幂等键、可恢复错误、终态集合和证据 URI。接口不存在时返回 `unsupported`，不得让模型杜撰成功结果。

推荐最小只读接口：资产搜索、表/字段详情、口径版本、上下游血缘、实例摘要、实例日志、SQL 计划。写接口按风险逐个开通，不使用超级管理员凭据；密钥进入企业密钥托管，不写入提示词、轨迹或 GitHub。

## 企业核验清单

- Dataphin 部署版本、Basic/Dev-Prod、发布审批和生产生效终态。
- OpenAPI 是否购买、SDK1/SDK2、实际可用操作、分页/限流/计费。
- MaxCompute 项目/Quota、只读角色、EXPLAIN 与诊断能力、成本口径。
- 元数据/血缘/质量的更新时间、缺口、权限裁剪和导出审批。
- 企业模型部署位置、数据保留、日志策略、上下文上限和不可出网保证。

