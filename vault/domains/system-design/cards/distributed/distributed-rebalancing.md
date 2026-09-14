---
id: distributed-rebalancing
node: distributed.partitioning.rebalancing
type: qa
---
## Q
How do you resplit/rebalance a sharded store without downtime, and what is the classic mistake in choosing partition count?

## A
Live migration recipe: (1) start copying the moving range to the new shard while (2) **dual-writing or streaming changes** (CDC) to keep it in sync, (3) when caught up, flip routing metadata atomically (router/config service), (4) drain and delete the old copy. Reads cut over per-range; writes must never be accepted in two places for the same range.

Classic mistake: `mod N` routing baked into clients, or too few fixed partitions. Standard designs: **many fixed logical partitions** mapped to fewer nodes (move whole partitions, never rehash), or **dynamic range splitting** (HBase/CockroachDB) that splits when a range grows hot or large.

## Q zh
怎样在不停机的情况下对一个分片存储做重新切分/再平衡？选择分区数量时的经典错误是什么？

## A zh
在线迁移的做法：(1) 开始把要搬迁的 range 拷贝到新分片，同时 (2) **双写或流式同步变更**（CDC）来保持同步，(3) 追上之后，原子地切换路由元数据（路由器/配置服务），(4) 排空并删除旧的那份拷贝。读按 range 逐个切换；对同一个 range，写永远不能同时在两个地方被接受。

经典错误：把 `mod N` 路由硬编码进客户端，或者固定分区数定得太少。标准做法：**大量固定的逻辑分区**映射到较少的节点上（搬迁整个分区，永远不重新哈希），或者**动态范围分裂**（HBase/CockroachDB），在一个 range 变热或变大时才分裂。
