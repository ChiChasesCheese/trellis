---
id: kafka-consumer-assign-vs-subscribe-exclusive
node: consumer.standalone
type: qa
source: kafka-2e
---
## Q
消费者可以调用 `subscribe()` 订阅主题（从而加入消费者群组），也可以调用 `assign()` 给自己直接指定要读取的分区。这两种方式能不能同时使用？

## A
不能。一个消费者要么通过 `subscribe()` 订阅主题、加入消费者群组，让 Kafka 自动分配分区并在群组变化时触发再均衡；要么通过 `assign()` 自己明确指定要读取哪些分区，完全跳过订阅和群组机制。二者是互斥的，只能选其中一种方式来确定消费者要读取的分区。
