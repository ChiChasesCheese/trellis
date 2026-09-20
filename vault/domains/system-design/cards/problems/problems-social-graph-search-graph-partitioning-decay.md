---
id: problems-social-graph-search-graph-partitioning-decay
node: problems.social.social-graph-search
type: qa
step: 1
tags: [grown]
---
## Q
In designing where to physically place a social graph's edges, why is co-locating densely-connected users on the same shard (community-aware graph partitioning) a weaker choice than simple hash partitioning by user id, even though it would reduce cross-shard traffic for local queries in theory?

## A
Finding an optimal graph partition (a minimum-cut style problem) is NP-hard at billions-of-nodes scale, and a real social graph continuously gains new edges, so any static partition computed today decays as the graph evolves — it would need repeated, expensive re-partitioning and data migration to stay effective. Hash partitioning by user id avoids this entirely: it gives predictable, even load and O(1) single-shard lookups for any one user's connections, accepting that a user's individual friends land on many different shards rather than trying to solve an NP-hard problem that would need constant maintenance anyway.

## Q zh
在决定社交关系图的边该物理存放在哪里时，为什么把连接紧密的用户共置到同一分片（社区感知的图分区）是比按用户 id 简单哈希分片更弱的选择，即便理论上它能减少局部查询的跨分片流量？

## A zh
在数十亿节点的规模下，找到最优图分区（一种最小割式的问题）本身是 NP 难问题，而真实的社交图谱在持续新增边，任何今天算出的静态分区都会随图的演化而腐化——需要反复、代价高昂地重新分区和迁移数据才能维持效果。按用户 id 哈希分片完全绕开了这个问题：它给出可预测、均匀的负载，以及任意单个用户连接的 O(1) 单分片查询，代价是接受一个用户的好友会散落在很多不同分片上，而不是去解一个本身就需要持续维护的 NP 难问题。
