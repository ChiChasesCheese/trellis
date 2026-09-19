---
id: kafka-admin-consumer-lag-calculation
node: admin.consumer-group-ops
type: qa
step: 1
source: kafka-2e
---
## Q
想知道一个消费者群组在某个分区上「落后了多少条消息」（consumer lag，消费滞后），需要结合调用 AdminClient 的哪两类方法、分别取哪个值来计算？

## A
先用 `listConsumerGroupOffsets` 拿到这个群组在每个分区上最近一次**提交的偏移量**（committed offset）；再用 `listOffsets` 并传入 `OffsetSpec.latest()`，拿到这个分区当前**最新消息的偏移量**（latest offset，即下一条要写入消息的位置）。两者相减（最新偏移量 − 已提交偏移量）就是这个消费者群组在该分区上还有多少条消息没有被消费，也就是消费滞后量。
