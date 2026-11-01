# 评测输入层

`evals/` 保存金标和行为合同，不保存运行结果。

- `cases.json`：40 条确定性开发回归用例，四类场景各 10 条。
- 用例固定合成快照、结构化工具动作、预期结果和引用要求。

运行 `python3 scripts/evaluate.py` 会读取本目录，并把结果写入 [`reports/evaluation.json`](../reports/evaluation.json) 与 [`reports/traces.json`](../reports/traces.json)。这些用例不评估通用 LLM 自然语言能力、生产权限或真实业务收益。
