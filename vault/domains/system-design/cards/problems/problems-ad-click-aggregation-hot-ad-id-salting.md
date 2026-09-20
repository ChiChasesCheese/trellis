---
id: problems-ad-click-aggregation-hot-ad-id-salting
node: problems.search.ad-click-aggregation
type: qa
step: 7
tags: [grown]
---
## Q
In an ad click aggregation design partitioned by `ad_id` for aggregation, what happens when a single ad campaign suddenly drives a disproportionate share of clicks, and how does the fix compare to merging Top-K results across shards?

## A
Because the aggregation stage partitions by `ad_id`, every click for that one viral campaign lands on a single shard, which becomes a processing hot spot while the rest of the cluster is comparatively idle. The fix mirrors a Top-K design's hot-item salting: detect the hot `ad_id` and append a random suffix (`ad_id + rand(0,N)`) to fan its clicks out across multiple sub-partitions that aggregate independently, then sum the sub-aggregates back together before writing to the OLAP store. Unlike merging Top-K candidate lists across shards, this merge is always exact — the sub-counts being summed are all counts for the same `ad_id`, so there's no risk of a candidate being missed, only ordinary addition.

## Q zh
在一个聚合阶段按 `ad_id` 分区的广告点击聚合设计中，当单个广告 campaign 突然占据了不成比例的点击量份额时会发生什么？这个修复手段和 Top-K 跨分片合并结果相比有什么不同？

## A zh
因为聚合阶段按 `ad_id` 分区，这一个爆量 campaign 的所有点击都会落在同一个分片上，该分片成为处理热点，而集群其余部分相对空闲。修复手段和 Top-K 设计里的热点 item 加盐是同一个思路：探测到热点 `ad_id` 后，给它拼上一个随机后缀（`ad_id + rand(0,N)`）把点击打散到多个独立聚合的子分区，写入 OLAP 之前再把各子聚合加总合并。和跨分片合并 Top-K 候选列表不同的是，这里的合并永远是精确的——被相加的各个子计数都是同一个 `ad_id` 的计数，不存在候选被遗漏的风险，只是普通的加法。
