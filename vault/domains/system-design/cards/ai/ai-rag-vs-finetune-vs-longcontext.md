---
id: ai-rag-vs-finetune-vs-longcontext
node: ai.rag
type: qa
---
## Q
To make an LLM answer from your company's data you can: RAG it, fine-tune on it, or stuff it all into the context window. When does each win?

## A
- **RAG**: default for **knowledge**. Wins when the corpus is large, changes often (update = re-index one doc, no retraining), needs **per-user access control** at retrieval time, or answers must cite sources.
- **Fine-tuning**: for **behavior, not facts** — style, format, domain jargon, tool-use patterns. Bad at knowledge: expensive to refresh, can't do permissions, can't cite, and facts get blended, not stored.
- **Long context**: fine when the corpus is small (fits comfortably), stable, and needed whole — but you pay its token cost and prefill latency **on every request**, and attention quality degrades over very long inputs.

Common production answer: RAG for facts, light fine-tune (or just prompting) for behavior.

## Q zh
为了让 LLM 从你公司的数据中回答，你可以：RAG 它、微调它或把它全部塞进上下文窗口。什么时候每个赢？

## A zh
- **RAG**：**知识** 的默认值。当语料库很大、经常变化（更新 = 重新索引一个文档，无需重新训练）、需要 **每个用户的访问控制** 在检索时，或答案必须引用源时赢。
- **微调**：对于 **行为，不是事实** — 风格、格式、领域行话、工具使用模式。在知识上很差：昂贵的刷新、无法做权限、无法引用，事实被混合，不存储。
- **长上下文**：当语料库很小（舒适地适合）、稳定且需要整体时很好 — 但你在 **每个请求上** 支付其 token 成本和预填充延迟，注意力质量在非常长的输入上下降。

常见的生产答案：RAG 用于事实，轻微调（或仅 prompting）用于行为。
