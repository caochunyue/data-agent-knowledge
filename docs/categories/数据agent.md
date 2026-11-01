# 数据agent

微信原文尚未采集。以下为官方资料知识卡；关注账号公开文章另有逐篇记录。

## Conversational Analytics API

- 来源：[google-data-agent](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/overview)；阅读状态：相关章节；证据：官方产品文档。
- 核心知识：提供结构化数据问答 API 和工具上下文；输出仍需验证。
- 应用方式：结合本库专题、固定业务样本和评测验证后采用。
- 限制：公开文档不证明本地部署成功，也不证明生产可靠性。

## Effective context engineering for AI agents

- 来源：[anthropic-context](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)；阅读状态：相关章节；证据：厂商工程文章。
- 核心知识：按任务选择上下文；扩大上下文不能替代相关性管理。
- 应用方式：结合本库专题、固定业务样本和评测验证后采用。
- 限制：公开文档不证明本地部署成功，也不证明生产可靠性。

## Demystifying evals for AI agents

- 来源：[anthropic-evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)；阅读状态：相关章节；证据：厂商工程文章。
- 核心知识：区分任务、trial、grader、轨迹与环境最终结果；评估模型和 harness 的组合。
- 应用方式：结合本库专题、固定业务样本和评测验证后采用。
- 限制：公开文档不证明本地部署成功，也不证明生产可靠性。

## Apache Ossie Ontology

- 来源：[ossie-ontology](https://github.com/apache/ossie/blob/48da55a07e4e8c3a11a662b14727557f6342536d/ontology/ontology.md)；阅读状态：相关章节；证据：规范草案。
- 核心知识：对象身份与业务关系分开建模；独立 mapping 已定义但工具支持存在缺口。
- 应用方式：结合本库专题、固定业务样本和评测验证后采用。
- 限制：公开文档不证明本地部署成功，也不证明生产可靠性。

## Apache Ossie Mapping schema

- 来源：[ossie-mapping](https://github.com/apache/ossie/blob/48da55a07e4e8c3a11a662b14727557f6342536d/ontology/mapping.json)；阅读状态：相关章节；证据：机器可读规范。
- 核心知识：独立映射引用一个 ontology 和一个 semantic model。
- 应用方式：结合本库专题、固定业务样本和评测验证后采用。
- 限制：公开文档不证明本地部署成功，也不证明生产可靠性。

## Shapes Constraint Language

- 来源：[shacl](https://www.w3.org/TR/shacl/)；阅读状态：相关章节；证据：W3C Recommendation。
- 核心知识：用 shape 验证 RDF 数据图；不是自动发现业务含义的工具。
- 应用方式：结合本库专题、固定业务样本和评测验证后采用。
- 限制：公开文档不证明本地部署成功，也不证明生产可靠性。


## 关注账号公开版本

- [评测也很酷，Data Agent 自动化评测的三层框架与实战](https://www.cnblogs.com/bytedata/p/19399354)（字节跳动数据平台，2025-12-25）：三层分别用于模型准入、组件定位与端到端业务评估；SQL 单快照同结果可能掩盖逻辑差异。
- [腾讯云大数据：从 AI-Ready 到 Agent-Ready，AI 原生数据底座全栈升级](https://cloud.tencent.com/developer/article/2687263)（腾讯云大数据，2026-06-11）：平台强调统一目录与多种检索能力，并将 SQL、代码、RAG 和报告能力组织为协作工具。
