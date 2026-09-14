---
id: async-dlq-poison-pill
node: async.delivery.guarantees
type: qa
---
## Q
When should a message go to a dead-letter queue, and what two things must you decide about the messages that land there?

## A
Move a message after **N failed attempts with backoff** when the failure is *non-transient* (malformed payload, business rule violation) — retrying a poison pill forever burns capacity and, in ordered/partitioned systems, blocks everything behind it.

Decisions:
- **Ordering**: DLQ'ing a message means later messages for the same key are processed first; you must either tolerate that or park the whole key.
- **Drain policy**: DLQ needs an owner, alerting, and a redrive path (fix + replay) — an unmonitored DLQ is just silent data loss with extra steps.

## Q zh
何时应该将消息发送到死信队列（DLQ），以及对于发送到那里的消息需要决定哪两件事？

## A zh
在**经过 N 次失败重试+退避后**，当故障是*非临时的*（格式错误的负载、业务规则违反）时，将消息移到 DLQ — 永远重试有毒消息会浪费容量，在有序/分区的系统中，会阻塞它后面的所有消息。

需要决定：
- **顺序**：DLQ 一条消息意味着同一 key 的后续消息被优先处理；你必须接受这一点或停泊整个 key。
- **清理策略**：DLQ 需要有所有者、告警和重放路径（修复 + 重放）— 无人监控的 DLQ 只是带着额外步骤的无声数据丢失。
