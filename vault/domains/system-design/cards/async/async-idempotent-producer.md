---
id: async-idempotent-producer
node: async.delivery.exactly-once
type: qa
---
## Q
Kafka's idempotent producer: what mechanism deduplicates, and which duplicates does it NOT eliminate?

## A
The broker assigns each producer a **producer id (PID)**; the producer stamps every batch with a **per-partition sequence number**. On a retry, the broker sees the sequence it already appended and discards the duplicate — exactly-once *append per producer session per partition*, on by default in modern Kafka.

It does NOT cover:
- **Application-level resends** — a new producer instance (new PID) after a crash, or your app calling `send()` twice.
- Duplicates from **consumer replays** downstream.

So it fixes broker-retry duplicates only; end-to-end dedup still needs [[correctness-idempotent-consumer-patterns]] or transactions.

## Q zh
Kafka 的幂等生产者：什么机制去重，哪些重复它*不*消除？

## A zh
broker 给每个生产者分配一个 **producer id（PID）**；生产者用 **per-partition 序列号**标记每个批次。重试时，broker 看到已经追加过的序列号并丢弃重复 — exactly-once *per producer session per partition*，在现代 Kafka 中默认开启。

它*不*覆盖：
- **应用级重发** — 崩溃后的新生产者实例（新 PID），或你的应用调用 `send()` 两次。
- **consumer 重放**下游的重复。

所以它只修复 broker-retry 重复；端到端去重仍然需要幂等 consumer 模式或 transaction。
