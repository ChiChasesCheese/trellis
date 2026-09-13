---
id: dist-regional-cache-eviction-policy
node: distributed.regional-cache
type: qa
---
## Q
A Redis cache shares memory between expiring content and nonexpiring control keys. `volatile-lru` starts returning OOM despite cold content. Why?

## A
`volatile-*` policies can evict only keys with TTL. If nonexpiring keys consume most memory, the evictable set may be exhausted and writes fail even though cold persistent keys remain. Separate cache and control workloads, or choose an `allkeys-*` policy only when every key is safely rebuildable. Reserve memory for replication and buffers, then monitor evictions, OOM errors, hit ratio, and object-size distribution together.

## Q zh
Redis cache 在同一内存中放 expiring content 和 nonexpiring control key。`volatile-lru` 即使存在冷内容仍开始 OOM。为什么？

## A zh
`volatile-*` policy 只能 eviction 带 TTL 的 key。若 nonexpiring key 占用大部分内存，可 eviction 集合会被耗尽，即使冷的 persistent key 仍存在，write 也会失败。应分离 cache 与 control workload；只有每个 key 都可安全重建时才选 `allkeys-*`。为 replication 和 buffer 预留内存，并同时监控 eviction、OOM error、hit ratio 与 object-size distribution。
