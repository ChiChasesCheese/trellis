---
id: async-exactly-once-myth
node: async.delivery.guarantees
type: qa
---
## Q
An interviewer asks: "Can a message broker give you exactly-once delivery?" What is the correct senior answer?

## A
No — **exactly-once *delivery* is impossible** over an unreliable network: if the ack is lost, the sender cannot distinguish "processed, ack lost" from "never processed", so it must either retry (duplicate) or not (loss).

What systems achieve is **effectively-exactly-once *processing***: at-least-once delivery + dedup at the consumer (idempotency keys, transactional offsets-plus-output as in Kafka transactions, or naturally idempotent writes). The guarantee lives at the endpoints, not in the pipe.

## Q zh
面试官问："消息 broker 能给你 exactly-once 投递吗？"正确的资深答案是什么？

## A zh
不能 — **exactly-once *投递*在不可靠网络上是不可能的**：如果 ack 丢失，发送者无法区分"已处理，ack 丢失"和"从不处理"，所以必须选择重试（重复）或不重试（丢失）。

系统实现的是**事实上 exactly-once *处理***：at-least-once 投递 + consumer 端去重（idempotency key、transactional offsets-plus-output 如 Kafka transactions、或天然幂等的写）。保证存在于端点，不在管道中。
