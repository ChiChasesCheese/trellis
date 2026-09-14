---
id: async-competing-consumers-ordering
node: async.queues
type: qa
---
## Q
Why do competing consumers on a classic queue destroy message ordering even though the queue is FIFO — and what are the fixes when per-entity order matters?

## A
FIFO only governs *dispatch*. With N consumers, messages for the same entity run **concurrently** (msg 2 can finish before msg 1), and a nack/redelivery re-enqueues a message *behind* ones sent after it. Prefetch buffers make the interleaving worse.

Fixes:
- **Partition by entity key** with one consumer per partition (Kafka model, SQS FIFO message groups).
- **Single-active consumer** per queue (RabbitMQ) — order preserved, parallelism sacrificed.
- Make consumers **order-tolerant**: version numbers + last-writer-wins or conditional updates, treating order as unguaranteed.

## Q zh
为什么在经典队列中竞争的 consumer 会破坏消息顺序，尽管队列是 FIFO — 当单个实体的顺序很重要时有什么解决办法？

## A zh
FIFO 只控制*分发*。有 N 个 consumer 时，同一实体的消息**并发运行**（msg 2 可能在 msg 1 之前完成），nack/redelivery 会把消息重新加入队列*后面*（在它之后发送的消息后面）。Prefetch 缓冲会让交错更糟。

解决办法：
- **按实体 key 分区**，每个分区一个 consumer（Kafka 模式、SQS FIFO 消息组）。
- **单活 consumer** 对应每个队列（RabbitMQ）— 顺序保证，但牺牲并行性。
- 让 consumer **容忍无序**：版本号 + last-writer-wins 或条件更新，把顺序当作无法保证的。
