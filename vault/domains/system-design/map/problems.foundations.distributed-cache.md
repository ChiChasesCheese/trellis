%% trellis:begin %%
# Distributed Cache
*Design Problems / Building Blocks & Warm-ups*

A Memcached/Redis-class cluster: sharding, eviction, hot keys, replication and cold-start.

**Requires:** [[domains/system-design/map/caching.invalidation|Invalidation & Eviction]], [[domains/system-design/map/distributed.partitioning.skew|Hot Keys & Skew]]

## Readings
- [[solution-distributed-cache|设计题解：分布式缓存（Distributed Cache，Memcached/Redis 风格）]]
- [[src-facebook-memcache-paper-distributed-cache|Scaling Memcache at Facebook]]
- [[src-netflix-evcache-distributed-cache|Caching for a Global Netflix]]
- [[src-redis-cluster-spec|Redis cluster specification]]

## Drills
- [[design-distributed-cache|Drill: Design a distributed cache (Memcached/Redis-class) in front of a database]]

## Cards (8)
1. [[problems-distributed-cache-fanout-multiplier-qps]]
2. [[problems-distributed-cache-lease-thundering-herd]]
3. [[problems-distributed-cache-sharding-tradeoffs]]
4. [[problems-distributed-cache-eviction-slab-vs-approx-lru]]
5. [[problems-distributed-cache-hot-key-mitigation]]
6. [[problems-distributed-cache-cold-start-peer-warm]]
7. [[problems-distributed-cache-durability-tradeoff-memcached-vs-redis]]
8. [[problems-distributed-cache-10x-hash-slot-granularity]]
%% trellis:end %%

## Notes
