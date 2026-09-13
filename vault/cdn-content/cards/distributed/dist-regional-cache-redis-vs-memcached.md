---
id: dist-regional-cache-redis-vs-memcached
node: distributed.regional-cache
type: qa
---
## Q
For a rebuildable regional content cache, when is Memcached enough, and when does Redis justify its extra operational surface?

## A
Memcached fits simple opaque key/value caching where loss is harmless, client-side sharding is acceptable, and no atomic data structure is needed. Choose Redis when the design requires atomic counters/scripts, richer values, replication/failover, or server-managed cluster behavior. Do not choose Redis merely for durability if the data is still a disposable cache; define source of truth, failure mode, eviction policy, and client timeout first.

## Q zh
对可重建的 regional content cache，什么时候 Memcached 足够，什么时候 Redis 的额外运维面值得？

## A zh
若只是简单 opaque key/value cache，丢失无害、可接受 client-side sharding，也不需要 atomic data structure，Memcached 足够。若设计需要 atomic counter/script、丰富 value、replication/failover 或 server-managed cluster behavior，再选 Redis。不要只因 durability 选择 Redis，而数据本质仍是 disposable cache；应先定义 source of truth、failure mode、eviction policy 和 client timeout。
