---
nodes: [ai.inference]
url: https://docs.vllm.ai/
tags: [reference, canonical]
---
# vLLM Documentation

The docs of the de-facto open-source LLM serving engine, and the best place
to learn serving concepts from the system that introduced them: PagedAttention
(KV cache managed like virtual memory) and continuous batching. Read the
design/architecture pages, not just the API reference.

**Extract on read:**
- Prefill (compute-bound, whole prompt at once) vs decode (memory-bandwidth-bound, token by token) — two different bottlenecks.
- PagedAttention: paging the KV cache kills fragmentation, so far more concurrent sequences fit per GPU.
- Continuous batching admits/retires sequences every step; prefix caching reuses KV for shared prompt prefixes.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.vllm.ai/)

## Archived copy
![[vllm-docs-clip]]
%% trellis:end %%
