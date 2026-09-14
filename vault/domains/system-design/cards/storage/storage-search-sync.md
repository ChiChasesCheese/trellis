---
id: storage-search-sync
node: storage.search
type: qa
---
## Q
How do you keep Elasticsearch/OpenSearch in sync with the primary database, and why is "write to both from the app" the wrong answer?

## A
Dual writes from the app have **no transaction spanning both stores**: a crash or failed second write leaves them silently diverged, and retries can reorder updates.

Standard answer: **CDC** — tail the DB's WAL/binlog (Debezium → Kafka → indexer) so the DB stays the single source of truth and the index is a derived, eventually consistent view; ordering per key comes from the log. Complement with periodic **full reindex/backfill** to heal drift and handle mapping changes (build a new index, then alias-swap).

## Q zh
你如何保持 Elasticsearch/OpenSearch 与主数据库同步，为什么"从应用写到两者"是错误答案？

## A zh
从应用的双写**没有跨越两个存储的事务**：崩溃或失败的第二次写让它们无声地分歧，重试可以重新排序更新。

标准答案：**CDC**——跟踪 DB 的 WAL/binlog（Debezium → Kafka → indexer），所以 DB 保持单个真实来源，索引是衍生的、最终一致的视图；每键排序来自日志。补充周期性**完整重索引/backfill** 来修复漂移并处理映射改变（构建新索引，然后别名交换）。
