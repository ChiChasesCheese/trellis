---
id: kafka-core-partition-ordering-scope
node: core.topics-partitions
type: qa
step: 2
source: kafka-2e
---
## Q
Kafka 保证「消息按顺序处理」，但这个顺序保证的范围有多大？一个包含4个分区的主题，能保证跨分区的消息也按发送顺序被读到吗？

## A
不能。Kafka 只保证消息在单个分区内的顺序：分区本质上是一段仅追加（append-only）的提交日志，消息按写入顺序追加到分区尾部，并按先入先出（FIFO）的顺序被读取。但一个主题通常包含多个分区，可能分布在不同服务器上被并行读写，因此同一主题内不同分区之间的消息没有全局顺序保证。
