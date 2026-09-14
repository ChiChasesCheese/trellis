---
id: caching-local-vs-remote
node: caching.placement
type: qa
---
## Q
In-process (local) cache vs shared remote cache (Redis): what do you gain and lose with each, and what pattern combines them?

## A
- **In-process**: ~100ns–1µs access, no network hop — but each instance holds its own copy (memory × N, cold on every deploy) and **cross-instance invalidation is hard**, so nodes can disagree.
- **Remote (Redis/Memcached)**: one consistent copy, survives app restarts, shared hit rate — but every read pays ~0.5–1ms network RTT and the cache is an infra dependency to size and fail over.

Combine as a **two-tier cache**: tiny local L1 with short TTL for the hottest keys, Redis as L2, often with pub/sub invalidation broadcasts to local tiers.

## Q zh
进程内（本地）缓存 vs 共享远程缓存（Redis）：每个优缺点是什么，什么模式结合它们？

## A zh
- **进程内**：~100ns–1µs 访问，无网络跳跃 — 但每个实例都有自己的副本（内存 × N，每次部署冷）并且 **跨实例失效很难**，所以节点可以不同意。
- **远程（Redis/Memcached）**：一个一致的副本，在应用重启后存活，共享命中率 — 但每次读支付 ~0.5–1ms 网络 RTT，缓存是需要调整大小和故障转移的基础设施依赖。

结合为 **两层缓存**：最热键的短 TTL 微小本地 L1，Redis 为 L2，通常与 pub/sub 失效广播到本地层。
