---
id: problems-distributed-cache-10x-hash-slot-granularity
node: problems.foundations.distributed-cache
type: qa
step: 8
tags: [grown]
---
## Q
In a Redis Cluster deployment sized at ~43 nodes for 200M DAU, what happens to per-node hash-slot granularity at 10x scale (2B DAU, ~421 nodes), given the cluster's fixed 16,384 total slots?

## A
At ~43 nodes, each node owns roughly 16,384/43 ≈ 381 slots on average. At ~421 nodes (peak ops scaled 10x from ≈4.2M to ≈42M, still at 100,000 ops/sec/node), each node's share drops to roughly 16,384/421 ≈ 38 slots — a 10x reduction in per-node slot granularity because the total slot count doesn't grow with the cluster. Each slot now represents a coarser chunk of the key space, making rebalancing and migration less fine-grained, which is part of why Redis's own documentation recommends keeping cluster size on the order of hundreds to about a thousand nodes rather than scaling this single-namespace design indefinitely.

## Q zh
在一个为 2 亿日活配置约 43 台节点的 Redis Cluster 部署中，给定集群固定 16,384 个总槽位，扩大到 10 倍规模（20 亿日活，约 421 台节点）时，每个节点的哈希槽粒度会发生什么变化？

## A zh
在约 43 台节点时，平均每个节点持有约 16,384/43 ≈ 381 个槽位。在约 421 台节点时（峰值操作数从约 420 万增长 10 倍到约 4,200 万，仍按每节点 10 万次/秒计算），每个节点的份额降到约 16,384/421 ≈ 38 个槽位——由于总槽位数不随集群增长，每节点的槽位粒度缩小了约 10 倍。每个槽位现在代表更粗粒度的一块 key 空间，让重分片和迁移的粒度变粗，这也是 Redis 官方文档建议把集群规模控制在几百到约一千台节点量级、而不是无限扩展这种单一命名空间设计的原因之一。
