## 目标与节奏

按你**有 Java 基础、能做基本前端页面、以求职转型为目标、每周投入 10–15 小时**设计，预计用 **10 个月**完成。最终交付一个可演示、可部署、可讲清架构取舍的 AI 全栈项目。

两条路线并行，但职责明确：**Java 负责业务系统与 Java AI 应用；Python 负责 Python AI 应用与 Agent 编排**。两边都亲手实现模型调用、RAG 和工具调用，再集成为一个产品。重点是 AI 应用工程，暂不安排模型训练。

## 学习与交付安排

| 阶段 | 时间 | Java + AI | Python + AI | 阶段交付 |
|---|---:|---|---|---|
| 基础打通 | 第 1–2 月 | Spring Boot API、认证、数据库、测试；接入模型并实现流式对话 | Python 类型、异步、Pydantic、FastAPI；实现同等的对话 API | 前端分别调用两套服务，完成对话与历史记录 |
| 知识库 | 第 3–4 月 | 用 Spring AI 实现文档入库、检索、引用来源的 RAG | 用 Python 实现相同流程，理解切分、向量检索和重排 | 两套可对比的知识库问答服务；建立固定问题集，记录答案质量与耗时 |
| Agent | 第 5–6 月 | 用 Spring AI 实现业务工具调用、权限控制和操作确认；了解 MCP | 用 LangGraph 实现多步骤工作流、状态保存、失败恢复和人工确认 | 能查资料并调用业务工具的 Agent；展示完整执行轨迹 |
| 全栈集成 | 第 7–8 月 | 负责用户、权限、业务数据、审计及统一 API | 负责复杂 Agent 工作流，并通过内部 API 调用 Java 业务能力 | React 或 Vue 前端 + Java 服务 + Python 服务 + 数据库的完整产品 |
| 求职打磨 | 第 9–10 月 | 补齐集成测试、限流、日志、部署与故障处理 | 补齐评测、成本统计、提示注入防护与工作流测试 | 在线演示、架构图、README、技术复盘和项目讲解材料 |

**主项目建议：企业知识库与工单助手。** 用户上传文档后可带引用地提问；Agent 能查询工单、生成处理建议，并在获得确认后执行受控操作。这个题目能同时展示前端、Java 业务后端、Python Agent、RAG、工具调用和工程化能力。

## 技术选择与学习方法

- **Java 路线：** Spring Boot + Spring AI + PostgreSQL。Spring AI 已覆盖模型调用、向量存储、工具调用和 MCP，适合作为主线；LangChain4j 放在后期对比学习，不同时深挖两个 Java 框架。[Spring AI 文档](https://docs.spring.io/spring-ai/reference/api/) · [LangChain4j 文档](https://docs.langchain4j.dev/intro/)
- **Python 路线：** FastAPI + Pydantic + LangGraph。先自己实现基础模型调用、RAG 和工具，再引入 Agent 框架，确保能解释每一步为何发生。FastAPI 提供清晰的 API 与类型校验学习路径。[FastAPI 教程](https://fastapi.tiangolo.com/tutorial/) · [LangChain 学习文档](https://docs.langchain.com/oss/python/learn)
- **每周分配：** Java 4 小时、Python 4 小时、共同项目 3–5 小时、复盘 1–2 小时。每两周产出一个能运行的功能；每月写一篇技术复盘，记录设计选择、测试结果和遇到的问题。

## 验收标准与默认假设

到第 10 个月，你应能独立演示两套 AI API，解释 RAG 检索效果与 Agent 工具调用过程，并展示完整产品的登录、对话、文档上传、工单操作、日志和部署。项目至少包含一组固定评测问题、关键流程自动化测试，以及一次失败案例分析。

默认使用你现有的 React 或 Vue 能力；模型供应商可按预算和可用性选择，项目通过配置切换。框架版本以实际开工时的官方文档为准。
