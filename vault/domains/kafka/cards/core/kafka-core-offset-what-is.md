---
id: kafka-core-offset-what-is
node: core.offsets
type: qa
step: 1
source: kafka-2e
---
## Q
Kafka 会给分区（partition，主题下的一段仅追加日志）里的每一条消息附加一个「偏移量」（offset）。这个偏移量到底标识的是什么？

## A
偏移量是 Kafka 在消息写入分区时附加的一个不断递增的整数元数据，用来标识这条消息在该分区内的位置，类似日志文件里「第几行」的编号。它不是消息内容的一部分，而是 Kafka 系统自己维护的位置标记，消费者靠它来定位和追踪自己读到了哪里。
