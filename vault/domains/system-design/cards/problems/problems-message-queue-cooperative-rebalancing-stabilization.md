---
id: problems-message-queue-cooperative-rebalancing-stabilization
node: problems.foundations.message-queue
type: qa
step: 5
tags: [grown]
---
## Q
In a Kafka-class consumer group's eager (stop-the-world) rebalance protocol, why does ANY single member joining or leaving force EVERY member to release ALL of its assigned partitions, and what does incremental cooperative rebalancing (KIP-429) change about this?

## A
Eager rebalancing works by incrementing a group generation id on any membership change and requiring every member to rejoin the new generation via JoinGroup/SyncGroup before receiving a fresh assignment; the protocol has no notion of a partition that does not need to move, so it revokes everything and recomputes globally, which a Confluent-published Kafka Connect benchmark (900 tasks across 3 workers) measured at 12-14 minutes to stabilize with all partitions unconsumed. Incremental cooperative rebalancing instead lets assignment converge over a few rounds: the coordinator only asks members to revoke the specific partitions that actually need to move to a different member, so partitions that keep the same owner are never interrupted -- the same benchmark scenario stabilized in about 1 minute with 2.13x higher aggregate throughput.

## Q zh
在 Kafka 一类消费者组的 eager（stop-the-world，停下整个世界）再平衡协议里，为什么任意一个成员的加入或离开都会强制所有成员释放它们全部已分配的分区？增量协作式再平衡（incremental cooperative rebalancing，KIP-429）改变了什么？

## A zh
Eager 再平衡的做法是：任何成员变更都会让组的世代号（generation id）递增，所有成员必须通过 JoinGroup/SyncGroup 重新加入新世代才能拿到新的分配——这个协议里没有「这个分区不需要移动」这个概念，所以每次都是全部释放、全局重算。Confluent 公开的一次 Kafka Connect 基准测试（900 个任务分布在 3 个 worker 上）测出这个过程要 12-14 分钟才能稳定，期间全部分区都未被消费。增量协作式再平衡则让分配在几轮内逐步收敛：协调者只要求那些真正需要换主的分区所在成员释放它们，其余分区的所有者不变、从未被打断——同样的基准场景下稳定时间降到约 1 分钟，聚合吞吐提升到 2.13 倍。
