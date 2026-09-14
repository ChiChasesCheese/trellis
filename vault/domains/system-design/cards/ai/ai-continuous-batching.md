---
id: ai-continuous-batching
node: ai.inference
type: qa
---
## Q
Why does LLM serving batch requests at the token level (continuous batching) instead of batching whole requests?

## A
GPUs are only efficient when work is batched, but LLM outputs have wildly different lengths. With **static batching**, the whole batch waits for its longest sequence — finished slots sit idle and new requests queue.

**Continuous (in-flight) batching** schedules per decode step: the moment a sequence emits its stop token, its slot is refilled with a waiting request. Utilization stays high regardless of length skew — the core scheduling idea behind vLLM/TGI-class servers and typically several-fold throughput over static batching.

## Q zh
LLM 服务为什么在 token 级别批处理请求（continuous batching）而不是批处理整个请求？

## A zh
GPU 只有在工作被批处理时才高效，但 LLM 输出的长度差异很大。使用 **static batching**，整个批次要等待最长的序列 — 已完成的槽位闲置，新请求排队。

**Continuous（在途）batching** 按 decode 步骤调度：一旦序列发出停止 token，其槽位就被等待中的请求填充。无论长度偏差如何，利用率都保持高位 — 这是 vLLM/TGI 级别服务器背后的核心调度思想，吞吐量通常是 static batching 的几倍。
