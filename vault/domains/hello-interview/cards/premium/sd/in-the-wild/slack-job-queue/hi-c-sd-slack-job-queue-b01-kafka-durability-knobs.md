---
id: hi-c-sd-slack-job-queue-b01-kafka-durability-knobs
node: sd.in-the-wild.slack-job-queue.beyond
type: qa
step: 1
---
## Q
**Slack 作业队列 · Kafka 不丢消息的几个开关**｜拓展 · 加分

"Kafka 不会丢消息"在什么条件下才成立？

## A
- **生产者的 `acks`：** `acks=1` 只等 leader 写入；`acks=all` 等所有同步副本（in-sync replicas，ISR）确认。前者低延迟但 leader 宕机可能丢。
- **`min.insync.replicas`：** 与 `acks=all` 配合，要求至少这么多副本同步才接受写入；副本因子 3、该值 2 是常见组合，允许挂一个 broker 而不丢也不停。
- **非干净选举：** 允许落后副本当 leader，换可用性、可能丢已确认的写入；默认关闭，需要的话得明确打开。
- **消费者提交偏移：** 先处理再提交 = 至少一次；先提交再处理 = 最多一次。要"恰好一次"需要事务或幂等消费。
- **面试说法：** 分别说清生产、复制、消费三段各自的保证，而不是笼统说"Kafka 持久"。
