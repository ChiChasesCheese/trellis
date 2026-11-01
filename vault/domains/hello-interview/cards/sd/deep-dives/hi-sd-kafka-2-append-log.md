---
id: hi-sd-kafka-2-append-log
node: qb.sd.job-scheduler-cron-history.pre-sd-deep-dives-kafka
type: qa
step: 2
---
## Q
**追加日志、offset 与复制**｜系统设计 · 深入技术

Kafka 的分区为什么设计成只追加的日志？offset 起什么作用？复制（replication）是怎么保证不丢数据的？

## A
**追加日志。** 不可变（只靠保留策略或日志压缩删除，不原地修改），简化复制、加快恢复、避免一致性问题；只在末尾写，减少磁盘寻道；方便靠加分区横向扩展。

**offset。** 消息在分区内的顺序编号。消费者读到哪里就提交 offset，重启后从上次提交处继续。

**复制。** 每个分区有一个 leader 副本，处理写（默认也处理读），其余 follower 副本在别的 broker 上持续同步。leader 挂了，控制器（controller）从已同步的 follower 里选出新 leader。

**易错。** 分区内的顺序由 offset 决定，不是时间戳。
