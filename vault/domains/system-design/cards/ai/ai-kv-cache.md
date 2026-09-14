---
id: ai-kv-cache
node: ai.inference
type: qa
---
## Q
What does the KV cache store, why is it the scarce resource in LLM serving, and what does prefix caching exploit?

## A
Per sequence, the attention **keys and values of every previous token**, so each new token attends without recomputing the past. It grows linearly with context length and concurrent sequences, and it competes with model weights for GPU memory — KV capacity, not compute, usually caps batch size (hence paged attention, which allocates it in blocks like virtual memory).

**Prefix caching**: sequences sharing a prefix (system prompt, few-shot examples, chat history) reuse one copy of that prefix's KV, skipping its prefill — large TTFT and cost wins for agent/chat workloads, and the mechanism behind API-level prompt caching discounts.

## Q zh
KV 缓存存储什么，为什么它是 LLM 服务中的稀缺资源，前缀缓存如何利用它？

## A zh
每个序列，注意 **前面每个 token 的键和值**，所以每个新 token 在不重新计算过去的情况下关注。它与上下文长度和并发序列线性增长，并与模型权重争夺 GPU 内存 — KV 容量，而不是计算，通常限制批大小（因此 paged attention，它像虚拟内存一样按块分配它）。

**前缀缓存**：共享前缀的序列（系统提示、小样本示例、聊天历史）重用该前缀的 KV 的一份副本，跳过其预填充 — 代理/聊天工作负载的大 TTFT 和成本收益，以及 API 级 prompt 缓存折扣背后的机制。
