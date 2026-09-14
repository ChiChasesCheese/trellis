---
id: correctness-outbox-cleanup
node: correctness.outbox
type: qa
---
## Q
An outbox table in Postgres receives every event the system emits. What operational problem builds up, and how do you clean it without breaking the pattern?

## A
Published rows accumulate: table and index **bloat**, MVCC dead tuples from delete/update churn, vacuum pressure, and slowing relay polls.

- **Delete-after-ack** (or CDC style: insert+delete in the same txn, relay reads the WAL insert) keeps the table near-empty but maximizes churn.
- **Mark sent + batch-purge** after a retention window — retention gives you a redelivery/debug buffer but keeps bloat.
- At high volume: **time-partitioned outbox table**, drop old partitions — `DROP PARTITION` is instant metadata work, no vacuum debt.

Never purge unpublished rows; purge eligibility = acked by the relay AND older than the dedup window your consumers rely on.

## Q zh
Postgres 的 outbox 表接收系统发的每个事件。什么运维问题积累，怎样不破坏模式地清理？

## A zh
已发布行积累：表和索引**膨胀**，删除/更新搅动的 MVCC 死元组，真空压力，relay 轮询减速。

- **ack 后删除**（或 CDC 风格：insert+delete 同一事务，relay 读 WAL 插入）让表接近空但最大化搅动。
- **标记已发送 + 保留窗口后批量清理** — 保留给你重传/调试缓冲但保持膨胀。
- 高量级：**时间分区 outbox 表**，删除老分区 — `DROP PARTITION` 是即时元数据工作，无真空债。

绝不清理未发布行；清理资格 = relay 已 ack AND 超过消费者依赖的去重窗口。
