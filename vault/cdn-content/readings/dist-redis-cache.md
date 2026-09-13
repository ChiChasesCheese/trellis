---
nodes: [distributed.regional-cache]
url: https://redis.io/docs/latest/develop/reference/eviction/
tags: [canonical]
---
# Redis key eviction

The official explanation of memory limits, LRU/LFU and volatile/allkeys policies, plus the operational buffers that make configured memory differ from usable cache capacity.

**Extract on read:**
- An eviction policy encodes whether every key is disposable.
- `volatile-*` cannot free nonexpiring keys and may become `noeviction` in practice.
- Hit ratio, evictions, OOM, object size, replication buffers, and headroom must be read together.

%% trellis:begin %%
## Source
[Open the original ↗](https://redis.io/docs/latest/develop/reference/eviction/)
%% trellis:end %%
