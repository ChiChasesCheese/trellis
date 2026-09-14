---
id: storage-wide-column-modeling
node: storage.nosql
type: qa
---
## Q
In Cassandra/DynamoDB-style wide-column stores, how does data modeling invert compared to relational, and what do partition key vs clustering (sort) key each decide?

## A
You model **query-first**: design one table per access pattern and denormalize, instead of normalizing then joining — there are no joins.

- **Partition key** → *which node/partition* the row lives on; every efficient query must supply it.
- **Clustering/sort key** → *order within the partition*, enabling range scans (e.g. `messages` partitioned by `channel_id`, clustered by `sent_at`).

What breaks: a query pattern you didn't design a table for needs a full scan or a new denormalized table backfilled.

## Q zh
在 Cassandra/DynamoDB 风格的宽列存储中，数据建模与关系型相比如何颠倒，分区键 vs 聚集（排序）键各决定什么？

## A zh
你建模**查询优先**：为每个访问模式设计一个表并非规范化，而不是规范化然后 join——没有 join。

- **分区键** → **哪个节点/分区**行住在；每个高效查询必须提供它。
- **聚集/排序键** → **分区内的顺序**，启用范围扫描（例如 `messages` 按 `channel_id` 分区，按 `sent_at` 聚集）。

什么破裂：你没设计表的查询模式需要完整扫描或新的非规范化表 backfill。
