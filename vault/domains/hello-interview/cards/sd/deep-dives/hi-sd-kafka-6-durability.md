---
id: hi-sd-kafka-6-durability
node: sd.deep-dives.kafka
type: qa
step: 6
---
## Q
**Kafka 的持久性与「消费者挂了」**｜系统设计 · 深入技术

Kafka 靠什么保证消息不丢？面试官问「Kafka 挂了怎么办」和「消费者挂了怎么办」，各该怎么回答？

## A
**持久性。** 每个分区多副本。生产者的 `acks=all` 表示等所有同步副本（ISR）都收到才确认，最强的持久保证；副本因子（replication factor）常用 3，即 1 个 leader 加 2 个 follower，坏一台仍可提升 follower。

**Kafka 挂了。** 通常认为 Kafka 始终可用（always available, sometimes consistent），这个问题不太现实，可以礼貌地反问。

**消费者挂了。** 这才更现实：
- offset：重启后从上次提交的 offset 继续，不丢但可能重处理（默认至少一次，at-least-once）
- 重平衡（rebalancing）：把它的分区转给组内其他消费者

**取舍。** 何时提交 offset：爬虫要等 HTML 存进 blob 存储后再提交；消费者做的事越多，失败后重做越多，所以让它的工作尽量小。
