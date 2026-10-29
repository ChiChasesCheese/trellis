---
id: uth-kafka-replication-3-unclean-election
node: kafka.replication
type: qa
step: 3
---
## Q
**ISR 全挂了，落后的副本能当 leader 吗**｜Kafka · 4.0

一个分区的 ISR 副本全部宕机，只剩落后的副本还活着，Kafka 能不能让它当 leader？

## A
**结构。** 由 `unclean.leader.election.enable` 决定，默认 `false`（0.11.0.0 起）：只有 ISR 成员有资格当 leader；设为 `true` 则允许落后副本“最后一搏”。

**细节。**

- 选 ISR 成员：保证拥有所有已提交（高水位以下）的消息，但 ISR 不恢复，分区就一直不可用。
- 选落后副本：分区马上可用，它的日志成为事实标准，却不保证含有每条已提交的消息，可能丢数据。

**为什么。** 这是可用性与一致性的二选一，基于投票的方案（如多数派）同样躲不开。

**对应 LeetCode：** 无直接对应的题（可用性与一致性的取舍）
