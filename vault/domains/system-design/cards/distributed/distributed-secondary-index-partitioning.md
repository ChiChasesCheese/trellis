---
id: distributed-secondary-index-partitioning
node: distributed.partitioning.indexes
type: qa
---
## Q
Local (document-partitioned) vs global (term-partitioned) secondary indexes on a sharded store — who pays, the writer or the reader?

## A
- **Local index**: each partition indexes only its own rows. Writes touch one partition (cheap, transactional with the row), but a query on the indexed field must **scatter-gather across every partition** — tail latency is the max over all shards.
- **Global index**: the index itself is partitioned by the indexed value (term), so a query hits one index partition. But one row update may touch **several index partitions**, so updates are typically **asynchronous** — the index lags the base data (DynamoDB GSIs work exactly like this, with their own provisioned throughput and eventual consistency).

Rule: write-heavy with occasional filtered reads → local; read-heavy queries on the secondary key → global, and accept the lag.

## Q zh
在一个分片存储上，本地（按文档分区）二级索引和全局（按词条分区）二级索引——付出代价的是写入方还是读取方？

## A zh
- **本地索引**：每个分区只为自己的行建索引。写入只碰一个分区（便宜，且和该行在同一个事务里），但对被索引字段的查询必须**跨每个分区做 scatter-gather**——尾部延迟等于所有分片里最慢的那个。
- **全局索引**：索引本身按被索引的值（词条）来分区，所以一次查询只打到一个索引分区。但一次行更新可能要碰到**好几个索引分区**，所以更新通常是**异步**的——索引会落后于 base data（DynamoDB 的 GSI 正是这样工作的，有自己独立的预置吞吐量，也是最终一致的）。

规则：写多、偶尔按二级属性过滤读 → 用本地索引；读多、频繁按二级 key 查询 → 用全局索引，并接受这个延迟。
