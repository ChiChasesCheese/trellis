---
id: kafka-core-message-key-partition-routing
node: core.topics-partitions
type: qa
step: 3
source: kafka-2e
---
## Q
生产者发送消息时可以附带一个可选的键（key，也是字节数组）。键有什么作用？两条键相同的消息一定会被分到同一个分区吗？

## A
键本身对 Kafka 没有特殊含义，但可以用来控制消息被写入哪个分区（partition，主题下的一段仅追加日志）：常见做法是对键计算一致性哈希值，再对主题的分区数取模，得到目标分区。只要分区数量不变，相同的键就会被哈希到同一个分区；但一旦分区数发生变化，同一个键就可能被路由到不同分区，所以「键相同必进同一分区」只在分区数不变的前提下成立。
