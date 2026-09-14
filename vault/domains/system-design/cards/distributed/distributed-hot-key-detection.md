---
id: distributed-hot-key-detection
node: distributed.partitioning.skew
type: qa
---
## Q
You suspect a hot key but can't emit a metric per key (billions of them). How do you actually find it, and at which layer?

## A
Use a **heavy-hitters sketch**, not per-key metrics: a **count-min sketch** or **space-saving / top-K** structure keeps the top N keys by frequency in fixed memory (kilobytes) with bounded error, flushed every few seconds. Put it in the layer that sees the raw key **before** partition routing — the client library, proxy/routing tier, or cache tier — so you learn the key even when the shard is already saturated.

Complements:

- **Sampled request logs** (1:1000) aggregated offline — finds yesterday's hot keys, not this second's.
- **Per-partition metrics** as the alarm, per-key sketch as the diagnosis: partition-level p99 or throttle counts tell you *which shard*, the sketch tells you *which key*.
- Managed equivalents: DynamoDB **CloudWatch Contributor Insights** reports the most-accessed partition keys directly.

The output must feed something automatic (promote to cache, enable salting for that key) — a dashboard a human reads is too slow for a key that goes hot in seconds.

## Q zh
你怀疑存在一个热 key，但没法给每个 key 都打点（有几十亿个）。你实际上怎么找到它？在哪一层找？

## A zh
用一个**heavy-hitters 概要结构**，而不是逐 key 打点：**count-min sketch** 或者 **space-saving / top-K** 结构能用固定大小的内存（几 KB）、带有界误差地保留按频率排序的前 N 个 key，每隔几秒刷新一次。把它放在能在**分区路由之前**看到原始 key 的那一层——客户端库、代理/路由层，或缓存层——这样即使分片已经饱和，你也能知道是哪个 key。

补充手段：

- **采样请求日志**（1:1000 抽样）离线聚合——能找到昨天的热 key，找不到这一秒的。
- **按分片的指标**用来报警，**按 key 的 sketch** 用来诊断：分片级别的 p99 或限流计数告诉你*是哪个分片*，sketch 告诉你*是哪个 key*。
- 托管系统的等价物：DynamoDB 的 **CloudWatch Contributor Insights** 会直接报告访问最多的分区键。

这个输出必须接到某个自动化动作上（提升到缓存、为该 key 启用 salting）——一个靠人去看的仪表盘，对一个几秒钟内就变热的 key 来说太慢了。
