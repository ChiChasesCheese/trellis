---
id: kafka-consumer-offset-commit-meaning
node: consumer.offset-commit
type: qa
step: 1
source: kafka-2e
---
## Q
Kafka 不像传统的 JMS 队列那样要求消费者对每条消息单独发送确认（ACK）。Kafka 消费者是靠什么机制来记录「已经处理到哪里了」？「提交偏移量」具体提交的是什么？

## A
Kafka 消费者靠更新自己在每个分区读取位置的「偏移量」来追踪消费进度，这个动作叫偏移量提交，做法是向 Kafka 内部的 `__consumer_offsets` 主题写入一条包含分区和偏移量的消息。提交并不是逐条确认，而是提交「已成功处理的最后一条消息」的偏移量（严格说是它的下一个位置），并假定这条消息之前的所有消息都已经被成功处理过。
