---
id: kafka-internals-time-index-purpose
node: internals.indexes
type: qa
source: kafka-2e
---
## Q
除了按偏移量（offset）查找消息，Kafka 还支持「给我某个时间戳之后的消息」这样的按时间查找需求，例如 Kafka Streams（Kafka 提供的流处理库）和某些故障转移场景就要用到。Kafka 靠什么机制支持这种查找，而不用整分区扫描时间戳？

## A
Kafka 为每个分区额外维护了一个**时间索引**，它建立的是「时间戳 → 消息偏移量」的映射。要按时间戳查找消息时，broker 先用时间索引把时间戳换算成对应的偏移量，再用偏移量索引（把偏移量映射到片段文件及文件内位置）定位到具体数据，两级索引配合，避免了对整个分区做逐条扫描来比对时间戳。
