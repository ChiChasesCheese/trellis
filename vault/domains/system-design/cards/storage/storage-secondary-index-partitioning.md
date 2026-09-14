---
id: storage-secondary-index-partitioning
node: storage.nosql
type: qa
---
## Q
In a partitioned store, secondary indexes can be local (document-partitioned) or global (term-partitioned). What does each cost, and which does DynamoDB's GSI use?

## A
- **Local**: each partition indexes only its own rows. Writes stay single-partition (index updated in the same operation), but a query on the indexed field must **scatter-gather across all partitions** — read latency = slowest partition, and cost grows with partition count.
- **Global**: the index itself is partitioned **by the indexed value**, so a query hits one partition. But one row's write now updates index partitions elsewhere — done **asynchronously**, so the index lags the base table.

DynamoDB GSIs are global: single-partition queries, eventually consistent, with their own provisioned capacity that can throttle base-table writes when hot.

## Q zh
在分区存储中，二级索引可以是本地（文档分区）或全局（词分区）。各花费什么，DynamoDB 的 GSI 使用哪个？

## A zh
- **本地**：每个分区仅索引自己的行。写保持单分区（索引在同一操作中更新），但在被索引字段上的查询必须**分散-聚集跨所有分区**——读延迟 = 最慢分区，成本随分区数增长。
- **全局**：索引本身按**被索引值**分区，所以查询命中一个分区。但一行写现在更新其他地方的索引分区——完成**异步**，所以索引滞后基表。

DynamoDB GSI 是全局的：单分区查询、最终一致、有自己的配置容量，当热时可以限流基表写。
