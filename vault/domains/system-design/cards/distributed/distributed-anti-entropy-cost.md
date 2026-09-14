---
id: distributed-anti-entropy-cost
node: distributed.replication.leaderless
type: qa
---
## Q
Anti-entropy repair is "just a background job" — what does it actually cost, and what breaks if you skip it for too long?

## A
Cost: each pair of replicas builds a **Merkle tree over its ranges** (full read of the data on disk — CPU + IO comparable to a table scan), exchanges hashes top-down, then streams only the differing leaf ranges. So the *comparison* is cheap in bandwidth but the **tree build is a full scan of every replica**, which is why full repair is scheduled off-peak and throttled, and why it is the dominant operational cost of large Cassandra clusters.

Skip it too long and you get **deleted data resurrecting**: deletes are tombstones with a grace period (`gc_grace_seconds`, 10 days by default). If a replica missed the tombstone and the tombstone is garbage-collected elsewhere before repair runs, that replica re-propagates the **old live value** and the row comes back. Rule: repair every range within the grace period, or raise the grace period.

## Q zh
反熵修复被当作"只是个后台任务"——它实际的代价是什么？如果拖太久不做会出什么问题？

## A zh
代价：每一对副本会为各自的范围**构建一棵 Merkle 树**（对磁盘上的数据做一次完整读取——CPU 和 IO 开销相当于一次全表扫描），自顶向下交换哈希值，然后只流式传输存在差异的叶子范围。所以*比较*本身在带宽上很便宜，但**构建树需要对每个副本做一次全量扫描**，这就是为什么完整修复要安排在非高峰期并做限流，也是大型 Cassandra 集群运维成本的主要来源。

拖得太久会导致**已删除的数据复活**：删除操作是带有宽限期的墓碑（tombstone，默认 `gc_grace_seconds` 为 10 天）。如果某个副本错过了这个墓碑，而墓碑在修复运行之前就在别处被垃圾回收了，那个副本就会把**旧的存活值**重新传播出去，这一行就复活了。规则：在宽限期内修复完每个范围，否则就调高宽限期。
