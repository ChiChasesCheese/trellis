---
id: problems-top-k-hot-item-salting
node: problems.search.top-k
type: qa
step: 7
tags: [grown]
---
## Q
In a Top-K design partitioned by hashing item_id, what happens to processing when a single item suddenly goes viral, and what's the standard mitigation?

## A
Because the partition key is item_id, every event for that one viral item lands on exactly one shard — that shard's stream processor becomes a hot spot doing far more work than the other shards, which sit comparatively idle, even though total cluster capacity is fine on average. The standard mitigation is to detect the hot key and salt it: append a random suffix (e.g. item_id + rand(0,15)) to fan that single item's events out across multiple sub-keys/partitions, counting each sub-key separately and summing the sub-counts back together to get the item's true count. This trades away the no-merge-needed property that item_id partitioning normally gives (see the exact K-way merge card) for a small, targeted merge, but only for the items detected as hot.

## Q zh
在一个按 item_id 哈希分区的热门榜设计中，当某个 item 突然爆红时处理会发生什么？标准的缓解手段是什么？

## A zh
因为分区 key 是 item_id，那个爆红 item 的所有事件都会落在同一个分片上——该分片的流处理器成为热点，承担的工作量远超其他分片，而其他分片相对空闲，即使集群总容量平均而言绰绰有余。标准的缓解手段是探测到热 key 后对其加盐：给 item_id 拼上一个随机后缀（例如 item_id + rand(0,15)），把这一个 item 的事件打散到多个子 key/分区上分别计数，再把各子计数加总得到该 item 的真实计数。这牺牲了 item_id 分区本来带来的「无需合并」的好处（换成需要一次小范围的合并），但只针对被探测为热点的 item。
