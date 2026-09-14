---
id: traffic-distributed-rate-limiting
node: traffic.rate-limiting
type: qa
---
## Q
Rate limit is 1,000 req/s per API key, enforced across 20 gateway instances. Compare the two enforcement designs and their failure trade-off.

## A
- **Centralized counters** (Redis, atomic Lua/INCR): exact global limit, but adds a network hop per request and the store becomes a hot dependency — decide **fail-open or fail-closed** when it's unreachable (usually fail-open: availability over strictness).
- **Local + async sync**: each node enforces ~limit/20 or a local bucket, reconciling counts in the background — zero added latency, survives store outages, but briefly over/under-admits as traffic skews across nodes.

Approximate local enforcement is the accepted norm; exactness is rarely worth a per-request round trip.

## Q zh
速率限制是每个 API 密钥 1,000 req/s，在 20 个网关实例中强制执行。比较两个执行设计及其故障权衡。

## A zh
- **集中化计数器**（Redis、原子 Lua/INCR）：确切的全局限制，但添加每个请求的网络跳跃且存储成为热依赖 — 决定当它不可达时**失败打开或失败关闭**（通常失败打开：可用性胜过严格性）。
- **本地 + 异步同步**：每个节点强制执行约限制/20 或本地存储桶，在后台协调计数 — 零添加延迟，存活存储故障，但随着流量在节点间倾斜时短暂过度/不足承认。

近似本地执行是公认的规范；精确性很少值得每个请求往返。
