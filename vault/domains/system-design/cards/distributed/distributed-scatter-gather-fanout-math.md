---
id: distributed-scatter-gather-fanout-math
node: distributed.partitioning.indexes
type: qa
---
## Q
A scatter-gather query fans out to 100 shards, each with a p99 of 10 ms. What is the query's latency distribution, and what do you do about it?

## A
The query finishes when the **slowest** shard replies, so you need *all* 100 under 10 ms: `0.99^100 ≈ 0.37`. About **63% of queries exceed 10 ms** — the per-shard p99 has become roughly the query's *median*. Generalize: fanout S turns the per-shard p(1−q) into a query-level exceedance of `1 − (1−q)^S`, so tail latency is amplified, not averaged.

Levers, in order of effectiveness:

- **Reduce S** — route on a key so the query hits 1 shard (the real fix; a global index or a query-shaped denormalized table).
- **Hedged/backup requests**: re-issue to a replica after the 95th percentile delay; costs a few % extra load and cuts the tail dramatically (Google's tail-at-scale result).
- **Partial results with a deadline**: return the shards that answered, flag incompleteness — acceptable for search/analytics, not for billing.

## Q zh
一次 scatter-gather 查询扇出到 100 个分片，每个分片的 p99 是 10 ms。这次查询的延迟分布会是什么样？你该怎么办？

## A zh
查询在**最慢**的那个分片回复时才算完成，所以你需要全部 100 个都在 10 ms 以内：`0.99^100 ≈ 0.37`。也就是说大约 **63% 的查询会超过 10 ms**——单个分片的 p99 差不多变成了整个查询的*中位数*。推广一下：扇出到 S 个分片，会把单个分片 `1−q` 的超出概率，放大成查询级别 `1 − (1−q)^S` 的超出概率，所以尾部延迟是被放大，而不是被平均掉。

按有效性排序的应对手段：

- **减小 S**——按某个 key 路由，让查询只打到 1 个分片（真正的修复方式；靠全局索引或按查询形状建的反规范化表）。
- **对冲/备份请求**：在 95 分位延迟之后，向另一个副本重新发起一次请求；多付出几个百分点的负载，却能大幅削减尾部（Google 的 tail-at-scale 结论）。
- **带截止时间的部分结果**：返回已经回答的分片，标记结果不完整——搜索/分析场景可以接受，计费场景不行。
