---
id: distributed-tenant-isolation-limits
node: distributed.partitioning.skew
type: qa
---
## Q
One tenant's runaway job saturates a shared shard and everyone on it gets timeouts. Which mechanisms contain the blast radius, and what does each actually bound?

## A
- **Per-key / per-tenant rate limits** (token bucket at the routing tier, keyed by tenant): bounds the *offender's* request rate, so the shard never saturates. Cheapest and first to reach for; needs a distributed counter (Redis or approximate local buckets with a global reconciliation).
- **Fair queueing / weighted admission** at the shard: bounds *share* rather than rate — under overload each tenant gets a slice instead of first-come-first-served, so a burst delays only its own owner.
- **Shuffle sharding**: assign each tenant a random *subset* of k nodes out of n. With n=8, k=2 there are 28 distinct pairs, so one abusive tenant fully overlaps with only ~1/28 of the others — the blast radius shrinks combinatorially without dedicated hardware per tenant.
- **Dedicated partitions** for the largest tenants: bounds everything, at the cost of capacity planning per tenant.

Escalation order: limit → fair-queue → shuffle-shard → isolate. Note limits must return a clean `429` with a retry hint, or clients turn the limit into a retry storm.

## Q zh
一个租户失控的任务打满了共享的分片，同一分片上的所有人都开始超时。哪些机制能控制爆炸半径？各自实际限制的是什么？

## A zh
- **按 key / 按租户的速率限制**（路由层的令牌桶，按租户区分）：限制的是*肇事者*的请求速率，让分片永远不会被打满。最便宜、最先该用的手段；需要一个分布式计数器（Redis，或者带全局对账的近似本地桶）。
- **分片上的公平排队 / 加权准入**：限制的是*份额*而不是速率——过载时每个租户分到一片，而不是先到先得，所以一次突发只会拖慢它自己的主人。
- **Shuffle sharding**：给每个租户随机分配 n 个节点中的 k 个作为子集。n=8、k=2 时有 28 种不同的组合，所以一个作恶的租户和其他租户的重叠只有大约 1/28——爆炸半径按组合数量级缩小，而不需要给每个租户配专属硬件。
- **给最大的租户配专属分区**：能限制住一切，代价是要按租户做容量规划。

升级顺序：限流 → 公平排队 → shuffle-shard → 隔离。注意限流必须返回干净的 `429` 并带重试提示，否则客户端会把限流变成一场重试风暴。
