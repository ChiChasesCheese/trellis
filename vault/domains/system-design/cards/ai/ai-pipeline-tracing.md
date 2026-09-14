---
id: ai-pipeline-tracing
node: ai.evals
type: qa
---
## Q
A user reports one bad answer from your RAG/agent pipeline (query rewrite → retrieve → rerank → generate → tool calls). What does AI-specific tracing capture, and what question must it answer?

## A
Same shape as distributed tracing — **one trace per request, a span per step** — but each span records the **full inputs and outputs** (prompts, retrieved chunks with scores, model responses), plus token counts, model version, latency, and cost.

The question it must answer: **which step failed?** Retrieval missed the doc vs reranker buried it vs the model ignored good context vs a tool call errored — each has a completely different fix, and without payloads in the trace they're indistinguishable.

Second job: traced failures become **new eval-set cases**, closing the loop between production and the offline suite. (OpenTelemetry has GenAI semantic conventions for exactly this.)

## Q zh
用户报告您的 RAG/agent 管道的一个错误答案（查询重写 → 检索 → 重新排名 → 生成 → 工具调用）。AI 特定的追踪捕获什么，它必须回答什么问题？

## A zh
与分布式追踪相同的形状 — **每个请求一个追踪，每个步骤一个 span** — 但每个 span 记录 **完整的输入和输出**（prompt、检索到的带评分的块、模型响应），加上 token 计数、模型版本、延迟和成本。

它必须回答的问题：**哪一步失败了？** 检索错过了文档 vs reranker 埋了它 vs 模型忽视了好上下文 vs 工具调用错误 — 每一个都有完全不同的修复，没有追踪中的负载它们是无法区分的。

第二项工作：被追踪的失败变成 **新的 eval-set 用例**，关闭生产和离线套件之间的循环。（OpenTelemetry 有 GenAI 语义约定正好用于此。）
