---
id: distributed-shard-key-one-way-door
node: distributed.partitioning.schemes
type: qa
---
## Q
Why is the shard key the highest-stakes decision in a sharded design, and what four properties do you check before committing to one?

## A
Because it is a **one-way door**: the key determines physical placement of every row, so changing it means rewriting the entire dataset. DynamoDB partition keys are immutable — you create a new table and backfill; MongoDB and Vitess have online resharding, but it's a multi-week migration with dual writes and a cutover, not a config change.

Check:

1. **High cardinality** — enough distinct values to exceed your eventual partition count.
2. **Even access distribution**, not just even data distribution (the two differ; a celebrity key is uniform in storage, hot in traffic).
3. **Query alignment** — the key appears in the predicate of your dominant read, or every read becomes scatter-gather.
4. **Transaction/locality alignment** — rows that must be mutated together (order + order_items) hash to the same partition, so you never need a distributed transaction.

Interview move: state the dominant query and the atomicity unit *first*, then derive the key from them.

## Q zh
为什么分片键是分片设计中风险最高的一个决策？在敲定它之前你要检查哪四个属性？

## A zh
因为它是一扇**单向门**：这个 key 决定了每一行数据的物理位置，所以改变它意味着重写整个数据集。DynamoDB 的分区键是不可变的——你只能新建一张表再回填数据；MongoDB 和 Vitess 有在线重新分片功能，但那是一次持续数周、带双写和切换的迁移，而不是一次配置变更。

要检查：

1. **高基数**——不同值的数量要足以超过你最终的分区数量。
2. **访问分布均匀**，不只是数据分布均匀（这两者不同；一个明星用户的 key 在存储上是均匀的，但在流量上是热点）。
3. **和查询对齐**——这个 key 要出现在你主要读路径的谓词里，否则每次读都会变成 scatter-gather。
4. **和事务/局部性对齐**——必须一起被修改的行（订单 + 订单项）要哈希到同一个分区，这样你就永远不需要分布式事务。

面试要点：先说清楚主导查询和原子性单元是什么，再从它们反推出分片键。
