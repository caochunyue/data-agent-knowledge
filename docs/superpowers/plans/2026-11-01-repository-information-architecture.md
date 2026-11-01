# Repository Information Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让整个数据 Agent 知识库按证据、知识、运行资产与报告形成可读、可验证的信息架构。

**Architecture:** 保持运行路径不变，以根 README、`docs/README.md` 与各主目录 README 构建分层导航；微信与 Ossie 分离，桥接层只记录映射规则。

**Tech Stack:** Markdown、JSON、Python 3.9 标准库现有校验器。

**Spec:** `docs/superpowers/specs/2026-11-01-repository-information-architecture-design.md`

## Global Constraints

- 不移动 `sources/`、`examples/`、`evals/`、`scripts/`、`tests/`、`reports/` 中被运行代码引用的文件。
- 不将公众号局部窗口观察升级为全文解析或完整覆盖。
- 保留现有 `reports/traces.json` 未提交改动。

## Review Focus

- 顶层目录入口应说明输入、输出和不承担的职责。
- 微信、Ossie、工程实践之间不得互相冒充来源。
- 状态页面不得继续写“微信原文 0”这类过期结论。
- 本地链接检查必须覆盖新 README。
- 评测和案例路径必须保持兼容。

### Task 1: 建立全仓导航与文档知识地图

**Files:**
- Create: `docs/README.md`, `docs/topics/README.md`, `docs/categories/README.md`
- Modify: `README.md`

- [ ] 写入目录职责、阅读顺序、跨域边界和历史文档映射。
- [ ] 运行 `scripts/validate_index.py`，确认本地 Markdown 链接通过。

### Task 2: 建立运行资产与证据目录入口

**Files:**
- Create: `evals/README.md`, `reports/README.md`, `scripts/README.md`, `templates/README.md`, `tests/README.md`
- Modify: `sources/README.md`, `examples/README.md`, `reports/acceptance.md`

- [ ] 写入每个目录的输入、输出、运行方式与边界。
- [ ] 修正微信窗口记录与覆盖闭合的状态表述。
- [ ] 运行单元测试和行为评测。

### Task 3: 最终审查与同步

**Files:** 所有上述改动。

- [ ] 检查链接、git diff、未提交用户文件边界。
- [ ] 提交并推送本次信息架构改动。
