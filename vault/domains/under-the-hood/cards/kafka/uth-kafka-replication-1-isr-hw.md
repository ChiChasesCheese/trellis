---
id: uth-kafka-replication-1-isr-hw
node: kafka.replication
type: qa
step: 1
---
## Q
**高水位与 ISR**｜Kafka · 4.0

消息写进 leader 后，消费者什么时候才读得到？一个副本落后到什么程度会被踢出 ISR？

## A
**结构。** 每个分区一个 leader 加若干 follower，follower 像消费者一样向 leader 拉取。ISR（in-sync replicas）是跟得上的副本集合；高水位（high watermark）是 ISR 内各副本日志末端（LEO）的最小值，消费者只能读到它之前的消息。

**细节。**

- `replica.lag.time.max.ms` 默认 30000：follower 超过 30 秒没追上 leader 末端，就被移出 ISR。
- 每当 follower 拉取进度更新，leader 就重算高水位（`maybeIncrementLeaderHW`）。

**为什么。** 对比多数派（如 Raft）：容忍 f 个故障，ISR 只要 f+1 个副本，多数派要 2f+1 个；代价是慢副本会拖住提交，所以要踢出 ISR。

**对应 LeetCode：** 无直接对应的题（复制协议的取舍）
