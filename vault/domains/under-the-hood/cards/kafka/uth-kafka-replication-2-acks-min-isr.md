---
id: uth-kafka-replication-2-acks-min-isr
node: kafka.replication
type: qa
step: 2
---
## Q
**acks=all 与 min.insync.replicas**｜Kafka · 4.0

副本因子 3、`acks=all`、`min.insync.replicas=2`：挂 1 台和挂 2 台 broker，写入分别会怎样？

## A
**结构。** `acks=all` 要求当前 ISR 里的副本全部确认；`min.insync.replicas` 规定 ISR 至少有几个，不够就拒绝写入。

**细节。**

- 挂 1 台：ISR 还剩 2 个，满足要求，照常写。
- 挂 2 台：ISR 只剩 1 个，leader 对 `acks=all` 的请求抛 `NotEnoughReplicasException`，高水位也不再前进。
- 生产者 `acks` 从 3.0 起默认 `all`（之前是 1）；`min.insync.replicas` 默认只有 1。

**坑。** “all”指当前 ISR 全体而非全部副本：ISR 缩到 1 个且 `min.insync.replicas=1` 时，`acks=all` 等于只写了 leader。

**对应 LeetCode：** 无直接对应的题（持久性与可用性的取舍）
