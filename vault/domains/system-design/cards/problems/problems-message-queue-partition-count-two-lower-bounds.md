---
id: problems-message-queue-partition-count-two-lower-bounds
node: problems.foundations.message-queue
type: qa
step: 1
tags: [grown]
---
## Q
In a Kafka-class distributed message queue sized for a peak write rate of about 2,777,778 messages/sec at 400 bytes each, why does a design that only computes partition count from write throughput (about 150 partitions at a 10MB/s-per-partition sequential-write budget) risk under-provisioning, even though 150 partitions is enough to absorb the peak write load?

## A
Partition count also has to satisfy a second, independent lower bound: the largest consumer group's maximum useful parallelism, since a partition can only be consumed by one instance within a given consumer group at a time. If the heaviest downstream consumer group needs roughly 556 parallel instances at peak (2,777,778 msgs/sec divided by an assumed 5,000 msgs/sec per instance), the topic needs at least that many partitions (rounded up to 600) regardless of what raw throughput alone would require -- and because reshuffling a key across a different number of partitions breaks that key's prior ordering guarantee, partition count must be set from the larger of the two bounds up front rather than grown incrementally later.

## Q zh
在一个按峰值写入速率约 2,777,778 条/秒（每条 400 字节）设计的 Kafka 一类分布式消息队列里，如果分区数只按写入吞吐来算（以每分区 10MB/s 的顺序写预算得到约 150 个分区），即便 150 个分区足以吸收峰值写入负载，为什么这种设计仍然有供给不足的风险？

## A zh
分区数还必须满足另一个独立的下限：下游最大消费者组的最大有效并行度——因为在同一个消费者组内，一个分区在同一时刻只能被一个实例消费。如果下游最重的消费者组在峰值下需要约 556 个并行实例（2,777,778 条/秒除以假设的每实例 5,000 条/秒），那么无论纯吞吐算出的下限是多少，这个主题都至少需要这么多分区（向上取整到 600）——而且因为把某个 key 重新哈希到不同数量的分区上会破坏该 key 此前的顺序保证，分区数必须一开始就按两个下限中较大的那个来定，而不能之后再逐步增长。
