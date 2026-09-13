---
nodes: [caching.eviction]
url: https://redis.io/docs/latest/develop/reference/eviction/
tags: [canonical, reference]
---
# Key Eviction (Redis Docs)

The official operational reference for memory limits and LRU, LFU, random, TTL-
scoped, and no-eviction policies. Read it as a policy decision, not a list of
configuration names.

**Extract on read:**
- Predict which key population each `maxmemory-policy` is allowed to evict.
- Choose LRU versus LFU from the workload's recency/frequency shape.
- Monitor hit ratio, evictions, memory, and miss cost while tuning policy.

%% trellis:begin %%
## Source
[Open the original ↗](https://redis.io/docs/latest/develop/reference/eviction/)
%% trellis:end %%
