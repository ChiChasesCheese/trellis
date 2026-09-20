---
nodes: [problems.realtime.llm-chat-service, ai.inference]
tags: [problem]
---
# Drill: Design an LLM chat service like ChatGPT

Design the backend for a ChatGPT-class product: users send messages, replies stream back
token by token, conversations span multiple turns, and free and paying users share the
same GPU fleet. Cover token streaming, the GPU serving tier, conversation state, admission
control and quotas, cost per request, safety filtering, and multi-region capacity.

**Constraints to state and honor**
- 20M DAU, 6 messages/user/day on average, ~5,556 peak QPS at a 4x day-peak factor.
- Model shape: 70B params, 80 layers, 8 KV heads (GQA), head dim 128, FP16 — KV cache
  cost is ~320 KiB/token; a 2,000-token session pins ~0.65 GB of GPU memory.
- A 4-GPU (80GB each) replica holds ~247 concurrent sessions after weights and overhead,
  which is the real cap on the serving tier, not GPU FLOPs.
- Free, Plus and Enterprise tiers share one GPU fleet; paying users' latency must not
  degrade when free-tier traffic surges.

**Grading points**
- Computes the KV cache bytes-per-token for a stated model shape and explains why that
  number, not compute, caps concurrent sessions per GPU replica
  ([[problems-llm-chat-service-kv-cache-bytes-per-token]]; builds on
  [[ai-kv-cache]] and [[ai-continuous-batching]] from Inference Serving rather than
  re-deriving what KV cache or continuous batching are).
- Explains why raw per-turn messages, not the assembled prompt, are the authoritative
  data, and what breaks if the assembled prompt were stored instead
  ([[problems-llm-chat-service-messages-vs-prompt-source-of-truth]]).
- Designs the dropped-connection path so a client disconnect does not cancel GPU
  generation, and describes the buffer-and-replay mechanism that lets a reconnect catch
  up ([[problems-llm-chat-service-disconnect-decoupled-from-generation]]).
- Argues for paged/block-based KV cache allocation over contiguous per-session
  allocation, and explains the fragmentation failure mode it avoids
  ([[problems-llm-chat-service-paged-kv-vs-contiguous]]).
- Argues for physically separating prefill and decode GPU pools over colocating them,
  with a concrete account of why one degrades the other
  ([[problems-llm-chat-service-prefill-decode-disaggregation-tradeoff]]).
- Designs admission control with per-tier reserved GPU capacity rather than a single
  global queue, and explains why per-user rate limiting alone isn't enough
  ([[problems-llm-chat-service-per-tier-reserved-capacity]]).
- Distinguishes a GPU node failure (unresumable, KV cache lost) from a dropped client
  connection (resumable), and gets the idempotency semantics right for each
  ([[problems-llm-chat-service-gpu-node-failure-unresumable]]).
- Explains what has to change about the scaling strategy at 10x DAU, beyond "add more
  GPUs" ([[problems-llm-chat-service-10x-model-routing-lever]]).

**Solution**: [[solution-llm-chat-service]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
