---
id: problems-message-queue-hot-partition-key-skew
node: problems.foundations.message-queue
type: qa
step: 7
tags: [grown]
---
## Q
In a Kafka-class message queue with 600 partitions, if a single large customer id concentrates enough traffic that 1% of partitions (6 partitions) absorb 20% of total write volume, why does simply increasing the total partition count fail to fix this hot spot, and what actually mitigates it?

## A
Every message for a given partition key always hashes to the same partition regardless of how many total partitions exist, so adding more partitions only spreads load for keys that are already well-distributed -- it does nothing for the traffic already concentrated on that one key's partition, which in this scenario would run at roughly 20x the uniform-average per-partition QPS (about 23,148 vs about 1,157 QPS/partition). Mitigation requires changing how that specific key is routed: either appending a random suffix to the hot key to spread its traffic across multiple partitions (at the cost of losing strict ordering for that key), or identifying the hot key ahead of time and routing it to a partition specifically provisioned with extra throughput headroom.

## Q zh
在一个有 600 个分区的 Kafka 一类消息队列里，如果某一个大客户 ID 集中了足够多的流量，导致 1% 的分区（6 个分区）吸收了 20% 的总写入量，为什么单纯增加总分区数解决不了这个热点？真正能缓解它的做法是什么？

## A zh
同一个分区键的每一条消息，无论总分区数是多少，永远哈希到同一个分区——所以增加分区数只能分散那些本来就分布均匀的 key 的负载，对已经集中在这一个 key 所在分区上的流量毫无帮助：在这个场景里，这个分区的 QPS 大约是均匀分布假设下每分区平均值的 20 倍（约 23,148 对比约每分区 1,157 QPS）。真正的缓解办法是改变这一个特定 key 的路由方式：要么给这个热 key 加随机后缀把它的流量打散到多个分区（代价是失去该 key 的严格顺序保证），要么提前识别出这个热 key，把它单独路由到一个专门预留了更大吞吐余量的分区。
