---
id: storage-tombstone-deletes
node: storage.nosql
type: qa
---
## Q
Why is a delete in Cassandra actually a *write*, and what makes "using a wide-column table as a queue" a famous anti-pattern?

## A
Data lives in immutable SSTables across replicas, so a delete writes a **tombstone** — a marker that shadows older values until compaction physically removes both, only after `gc_grace_seconds` (default ~10 days, kept so a down replica can learn of the delete; purge earlier and the value **resurrects** via read repair or the recovered replica).

Queue anti-pattern: enqueue-then-delete leaves partitions that are mostly tombstones; every read must scan **thousands of tombstones to find one live row**, latency climbs until reads abort (`tombstone_failure_threshold`). Rapid create-delete churn belongs in a log/queue (Kafka), not an LSM wide-column store.

## Q zh
为什么 Cassandra 中的删除实际上是一个**写**，什么让"用宽列表作队列"成为著名反模式？

## A zh
数据住在跨副本的不可变 SSTable，所以删除写一个**墓碑**——一个遮蔽旧值直到压实物理移除两者的标记，仅在 `gc_grace_seconds` 后（默认 ~10 天，保持以便关闭副本可以了解删除；更早清除，值通过读修复或恢复的副本**复活**）。

队列反模式：enqueue-then-delete 留下主要是墓碑的分区；每个读必须扫描**数千个墓碑找一个活行**，延迟爬升直到读中止（`tombstone_failure_threshold`）。快速创建-删除流失属于日志/队列（Kafka），不是 LSM 宽列存储。
