---
id: async-log-vs-queue
node: async.log
type: qa
---
## Q
What does an append-only log (Kafka) give you that a traditional broker queue (RabbitMQ/SQS) fundamentally cannot?

## A
**Replay.** A queue deletes messages on ack; the log retains them for a retention window (or forever with compaction), and consumers just track offsets.

That enables:
- **Rebuilding derived state** (new index, new materialized view, bug fix) by re-reading from offset 0.
- **Multiple independent consumer groups** reading the same history at their own pace.
- The log acting as **system of record** for event-sourced designs.

Trade-off: no per-message ack/retry/DLQ semantics built in — a stuck message blocks its partition (head-of-line blocking).

## Q zh
append-only log（Kafka）给你什么传统 broker 队列（RabbitMQ/SQS）根本无法提供？

## A zh
**Replay。** 队列在 ack 时删除消息；日志在保留窗口内保留它们（或使用压缩永久保留），consumer 只追踪 offset。

这使得能够：
- **重建派生状态**（新索引、新物化视图、bug 修复）通过从 offset 0 重新读取。
- **多个独立 consumer group** 以自己的速度读取相同历史。
- 日志作为**记录系统**用于事件溯源设计。

权衡：内置没有 per-message ack/retry/DLQ 语义 — 卡住的消息阻塞其 partition（head-of-line 阻塞）。
