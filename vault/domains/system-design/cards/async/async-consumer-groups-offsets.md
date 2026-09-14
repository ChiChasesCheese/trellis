---
id: async-consumer-groups-offsets
node: async.log
type: qa
---
## Q
In a Kafka consumer group, when should you commit offsets relative to processing, and what does each choice cost you?

## A
- **Commit after processing** → at-least-once: a crash between process and commit replays messages, so downstream must be idempotent. This is the default correct choice.
- **Commit before processing** → at-most-once: a crash loses messages. Only acceptable for droppable data (metrics, best-effort notifications).
- Also know: parallelism is capped at partition count — one partition is consumed by at most one member of a group, so 20 consumers on 10 partitions leaves 10 idle.

## Q zh
在 Kafka consumer group 中，何时应该相对于处理来提交 offset，每种选择的代价是什么？

## A zh
- **处理后提交** → at-least-once：处理和提交之间发生崩溃会导致消息重新投递，所以下游必须是幂等的。这是默认的正确选择。
- **处理前提交** → at-most-once：崩溃会丢失消息。只能用于可丢弃的数据（指标、尽力而为的通知）。
- 另外要知道：并行度受 partition 数量限制 — 一个 partition 最多被 group 中的一个成员消费，所以 20 个 consumer 对应 10 个 partition 会留下 10 个 idle。
