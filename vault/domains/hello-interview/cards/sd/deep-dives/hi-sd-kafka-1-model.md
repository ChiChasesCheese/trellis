---
id: hi-sd-kafka-1-model
node: qb.sd.job-scheduler-cron-history.pre-sd-deep-dives-kafka
type: qa
step: 1
---
## Q
**Kafka 的核心模型：broker、topic、partition、消费者组**｜系统设计 · 深入技术

Kafka 里的 broker、topic、partition、producer、consumer group 分别是什么？为什么说分区才是它扩展的方式？

## A
**组成。**
- broker：集群里的一台服务器，负责存数据、服务客户端
- partition：有序、不可变、持续追加的消息序列，像一个日志文件，物理上分布在各 broker
- topic：若干分区的逻辑分组，发布与订阅都以 topic 为单位
- 消费者组（consumer group）：每个分区在组内只分给一个消费者，所以正常情况下一条消息只被组内一个消费者处理

**为什么。** 分区允许并行消费，数据按 key 路由到分区，同一 key 的消息保持顺序，多个分区则可以并行处理，这是顺序与吞吐的折中。

**区别。** topic 是逻辑分组，partition 是物理分组。
