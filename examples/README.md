# 可运行的工具 Harness 案例

从仓库根目录执行 README 中命令。基础案例 Python 3.9+，无第三方依赖。每次 Harness 从 seed.sql 建立新的内存 SQLite，不写真实数据库。

| 工具 | JSON 输入 | 返回 |
|---|---|---|
| search | tool=search, query | 资产 IDs、知识卡与来源 |
| metric | tool=metric, name | 值、单位、口径和引用，或 clarify |
| sql | tool=sql, sql | 查询行或结构化 error |
| entity | tool=entity, tenant_id, customer_id | 完整身份、属性和来源 |
| relationship | tool=relationship, tenant_id, order_id | placed_by 事实、证据、映射版本 |

目录 exact synonym 检索只演示可引用资产；不是 RAG 排序系统。指标模板是批准 SQL；不是通用自然语言 SQL 生成。实体映射从 model.json 读取；不是通用 Ossie 执行器。

## 预期结果

- paid_revenue：37000 分，即 370 CNY；paid_order_count：3。
- 只按 customer_id 关联得到 8 行；加 tenant_id 正确得到 5 行。
- tenant a/customer 1 与 tenant b/customer 1 是不同对象；共享邮箱不能合并客户。
- DELETE、DDL、ATTACH、PRAGMA、多语句、扩展加载拒绝；递归失控查询由 VM 预算终止；调用预算耗尽返回错误；结果超行数返回 row_limit。

本例不做真实用户鉴权，SQL 可访问全部合成租户；tenant_id 不是授权凭据。SQLite 限制不构成进程或内核隔离，VM 计数也不等于墙钟时间上限。只接受受控教学输入，不暴露为公网 SQL 服务。

## Ossie 格式示例与校验

commerce.semantic.json / commerce.ontology.json / commerce.mapping.json 为三个独立文档；schemas 保存固定提交的官方 JSON Schema 和许可证，provenance.json 保存哈希。JSON 是规范支持的格式，不需要 YAML 解析器。

可选依赖仅供 schema 验证：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-validation.txt
.venv/bin/python scripts/validate_ossie.py
```

验证器使用离线 registry 将上游 main URI 解析到固定快照，避免远程漂移；验证 schema 结构、哈希和目标文档名字，不编译 SQL，不证明全部概念/字段引用正确或运行时语义等价。基础行为评测与此检查独立报告。

## 模型接入扩展点（未实现）

把模型限定为输出允许的工具动作，经 Harness 验证后执行，再将工具证据交还模型生成有引用答复。不得向模型传入 evals 的 expected 字段。先建立新的保留问句集、真实权限上下文及多次 trial，再衡量模型正确率和成本；当前 40 条仅作开发回归。
