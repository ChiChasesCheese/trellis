---
id: caching-memcached-vs-redis
node: caching.strategies
type: qa
---
## Q
When is Memcached the right pick over Redis, and what does Redis add that decides most other cases?

## A
**Memcached**: multithreaded (one instance saturates all cores), simple slab-allocated LRU byte cache, very flat performance — right when the job is purely a look-aside blob cache at huge scale (Facebook's use).

**Redis/Valkey** adds: data structures (hashes, sorted sets, lists), atomic ops + Lua, per-key TTL with richer eviction, replication + failover + optional persistence, pub/sub and streams — right when the "cache" also does ranking, counters, sessions, locks, or queues. Being single-threaded per core, it scales by sharding instead.

2026 default: Redis/Valkey, unless the workload is strictly bytes-in/bytes-out at extreme throughput.

## Q zh
什么时候 Memcached 是正确的选择而不是 Redis，Redis 添加什么决定了大多数其他情况？

## A zh
**Memcached**：多线程（一个实例饱和所有核），简单 slab 分配的 LRU 字节缓存，非常平坦的性能 — 正确当作业是纯粹的大规模旁路 blob 缓存时（Facebook 的使用）。

**Redis/Valkey** 添加：数据结构（哈希、有序集、列表）、原子操作+Lua、每键 TTL 有更丰富的驱逐、复制+故障转移+可选持久性、pub/sub 和流 — 正确当"缓存"也做排名、计数器、会话、锁或队列时。作为单线程每个核，它通过分片缩放。

2026 默认：Redis/Valkey，除非工作负载是严格的 bytes-in/bytes-out 在极端吞吐量下。
