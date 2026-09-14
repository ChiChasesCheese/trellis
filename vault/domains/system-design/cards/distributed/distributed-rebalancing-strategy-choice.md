---
id: distributed-rebalancing-strategy-choice
node: distributed.partitioning.rebalancing
type: qa
---
## Q
Three rebalancing strategies — fixed total partition count, dynamic split/merge, and a fixed number of partitions *per node* — each hold a different quantity constant. Which, and how does that decide the choice?

## A
- **Fixed total count** (Kafka topics, Elasticsearch shards): the *number of partitions* is constant; partition **size grows with data**. Choose when you can predict scale well enough to pre-size, and you value the simplest possible move operation (reassign whole partitions, mapping never changes).
- **Dynamic split/merge** (HBase, CockroachDB): *partition size* stays within bounds; the **count tracks data volume**. Choose for unpredictable or wide-ranging growth (1 GB → 100 TB with no re-provisioning), and it's the only strategy that adapts range partitions to where the keys actually are.
- **Per-node fixed count** (Cassandra-style vnodes): *partitions per node* is constant; a joining node **splits/steals random ranges** from others, so per-partition size stays proportional to per-node data. Requires hash partitioning (random split points are only fair on hashed keys). Choose for homogeneous, incrementally-scaled clusters where per-node overhead should stay flat.

Common failure: fixed count picked too small early on becomes a hard ceiling — the reason the other two exist.

## Q zh
三种 rebalancing 策略——固定的分区总数、动态 split/merge、每个节点固定的分区数——各自把一个不同的量保持恒定。分别是哪个量？这如何决定选型？

## A zh
- **固定总数**（Kafka topic、Elasticsearch shard）：*分区数量*恒定，分区**大小随数据增长**。适用于规模可以预估、可以预先定容的场景，并且你想要最简单的迁移操作（整分区重新指派，key 到分区的映射永不变化）。
- **动态 split/merge**（HBase、CockroachDB）：*分区大小*保持在阈值内，**数量跟随数据量**。适用于不可预测或跨度极大的增长（1 GB 到 100 TB 无需重新规划），而且它是唯一能让 range 分区贴合 key 实际分布的策略。
- **每节点固定数**（Cassandra 式 vnode）：*每个节点的分区数*恒定；新节点加入时**随机拆分/接管**其他节点的部分区间，所以单个分区的大小与单节点数据量成正比。它要求 hash 分区（随机切分点只有在哈希过的 key 空间上才公平）。适用于同构、逐台扩容、希望单节点开销保持平稳的集群。
- 常见翻车：早期把固定总数定得太小，日后成为硬上限——这正是另外两种策略存在的原因。
