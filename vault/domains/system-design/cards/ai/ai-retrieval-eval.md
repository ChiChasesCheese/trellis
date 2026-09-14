---
id: ai-retrieval-eval
node: ai.vector-search
type: qa
---
## Q
You want to change chunk size and swap the embedding model in your RAG system. How do offline and online evaluation divide the work of proving it's an improvement?

## A
- **Offline**: a **golden set** of real queries with labeled relevant docs; measure recall@k, MRR/nDCG per candidate config in minutes. This *gates* changes — cheap, reproducible, runs in CI — but only as good as the label set, which drifts from live traffic.
- **Online**: ship behind an experiment; measure end-task metrics — answer quality (thumbs, LLM-as-judge on grounded-ness), deflection/click-through, "no-answer" rate. This *validates* what offline can't see (query drift, latency effects on abandonment), but is slow and noisy.

Discipline: offline eval to kill bad candidates fast, online to confirm the survivor; continuously **harvest failed prod queries back into the golden set** so offline stays honest.

## Q zh
你想改变 RAG 系统中的块大小并交换 embedding 模型。离线和在线评估如何分工来证明这是一项改进？

## A zh
- **离线**：具有标记的相关文档的真实查询的 **黄金集**；在几分钟内测量每个候选配置的 recall@k、MRR/nDCG。这 *控制* 更改 — 廉价、可重复、在 CI 中运行 — 但仅与标签集一样好，标签集从实时流量中漂移。
- **在线**：在实验后发货；测量终端任务指标 — 答案质量（点赞、LLM-as-judge on groundedness）、偏转/点击率、"无答案"率。这 *验证* 了离线看不到的（查询漂移、延迟对放弃的影响），但速度慢且嘈杂。

纪律：离线 eval 快速杀死坏候选者，在线确认幸存者；持续 **收获失败的生产查询回到黄金集** 所以离线保持诚实。
