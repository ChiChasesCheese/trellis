---
id: uth-kafka-zero-copy-3-batch-compress
node: kafka.zero-copy
type: qa
step: 3
---
## Q
**批量与压缩：把小消息攒成大块**｜Kafka · 4.0

生产者发 10 万条小消息，Kafka 怎么避免 10 万次小 I/O？批次什么时候发出？

## A
**结构。** 生产者按分区攒批（`RecordBatch`）。批是网络传输、磁盘存储、压缩的共同单位：整批压缩，broker 解压校验后仍以压缩态落盘，消费者才解压。

**细节。**

- 批次满 `batch.size`（默认 16384 字节）或等满 `linger.ms` 就发；`linger.ms` 从 4.0 起默认 5，之前是 0。
- `compression.type` 默认 `none`。

**坑。** `linger.ms=0` 时只有生产者忙不过来才被动成批。

**为什么。** 重复内容（如 JSON 字段名）散在消息之间，逐条压缩效果很差；成批后随机小写变成顺序大块，才配得上页缓存和 `sendfile`。

**对应 LeetCode：** 无直接对应的题（批处理的工程取舍）
