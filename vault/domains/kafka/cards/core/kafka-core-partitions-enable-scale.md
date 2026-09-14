---
id: kafka-core-partitions-enable-scale
node: core.topics-partitions
type: qa
source: kafka-2e
---
## Q
主题（topic，消息的分类单位，类似数据库里的表）为什么要被划分成多个分区（partition）？这对 Kafka 的横向扩展能力有什么帮助？

## A
分区是 Kafka 实现数据冗余和横向伸缩的手段：一个主题的多个分区可以分布在不同的服务器上，使该主题的总吞吐量不受限于单台服务器的性能，多台机器可以并行处理不同分区的读写；同时，同一分区可以有多个副本保存在不同服务器上，防止某台服务器故障导致数据丢失。分区数量越多，理论上可并行参与该主题读写的服务器和消费者也越多。
