---
id: distributed-hash-vs-range
node: distributed.partitioning.schemes
type: qa
---
## Q
Hash partitioning vs range partitioning: what does each optimize, and what workload wrecks each?

## A
- **Hash**: uniform key spread → even load, no planning. Wrecked by **range queries** — "last hour of events" scatters across every shard (scatter-gather).
- **Range**: adjacent keys co-located → efficient range scans, and shards can split where data actually is. Wrecked by **monotonically increasing keys** (timestamps, sequential IDs) — all inserts hammer the last shard (hot tail).

Standard hybrid: **hash a prefix, range the rest** — e.g. partition by `hash(user_id)`, sort by `timestamp` within the partition (DynamoDB's PK/SK, Cassandra's partition + clustering keys): even spread across users, cheap time-range scans per user.

## Q zh
哈希分片和范围分片：各自优化的是什么？各自的工作负载杀手是什么？

## A zh
- **哈希（Hash）**：key 均匀分布 → 负载均衡，不需要规划。杀手是**范围查询**——"过去一小时的事件"会散落到每一个分片上（scatter-gather）。
- **范围（Range）**：相邻的 key 放在一起 → 范围扫描高效，而且分片可以在数据实际所在的地方切分。杀手是**单调递增的 key**（时间戳、自增 ID）——所有插入都砸向最后一个分片（热尾，hot tail）。

标准的混合方案：**前缀用哈希，其余用范围**——比如按 `hash(user_id)` 分区，分区内部按 `timestamp` 排序（DynamoDB 的 PK/SK、Cassandra 的 partition key + clustering key）：跨用户均匀分布，同时每个用户的时间范围扫描又很便宜。
