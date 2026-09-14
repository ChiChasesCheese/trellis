---
id: join-strategy-failure-modes
node: query.join-strategies-broadcast-shuffle
type: qa
tags: [grown]
---
## Q
连接策略选错或数据分布不均时，分别会出现什么典型症状？

## A
① 本以为很小的一侧实际很大却被广播：每个节点都要容纳整张表并构建哈希表，内存吃紧，出现溢出（spilling）甚至大量网络传输，查询骤慢。② 洗牌连接遇到连接键倾斜（skew，某个键值出现极多）：哈希重分布把这些行全部送到同一个节点，该节点成为热点，其余节点空闲，整体耗时由最慢的节点决定。在查询画像中可见某个 Join 或其输入节点耗时远超其他。
