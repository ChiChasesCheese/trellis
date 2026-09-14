---
id: async-retry-delay-implementation
node: async.queues
type: qa
---
## Q
Your consumer needs retries with backoff (5s, 1m, 10m), but the broker delivers immediately. How is delayed retry actually implemented, and what does it cost you?

## A
- **Kafka**: no native delay — use **tiered retry topics** (`orders-retry-5s`, `-1m`, `-10m`); a failed message is republished to the next tier, whose consumer pauses until the message's due time, then finally to the DLQ.
- **RabbitMQ**: per-message TTL + dead-letter exchange, or the delayed-message plugin.
- **SQS**: native per-message delay / visibility-timeout extension — simplest option.

Cost: the message **leaves its original ordering context** — anything behind it proceeds, so retried messages are processed out of order and consumers must tolerate that (version checks, idempotency). If strict per-key order matters, you must instead block the key (or partition) while retrying in place.

## Q zh
你的 consumer 需要有退避的重试（5s、1m、10m），但 broker 立即投递。延迟重试实际如何实现，对你的代价是什么？

## A zh
- **Kafka**：无原生延迟 — 使用**分层重试 topic**（`orders-retry-5s`、`-1m`、`-10m`）；失败消息重新发布到下一层，其 consumer 暂停直到消息的到期时间，然后最后到 DLQ。
- **RabbitMQ**：per-message TTL + dead-letter exchange，或 delayed-message 插件。
- **SQS**：原生 per-message 延迟 / visibility-timeout 扩展 — 最简单选项。

代价：消息**离开原始排序上下文** — 它后面的任何东西都继续，所以重试消息无序处理，consumer 必须容忍（版本检查、幂等性）。如果严格的 per-key 顺序重要，你必须改为在原地重试时阻塞 key（或 partition）。
