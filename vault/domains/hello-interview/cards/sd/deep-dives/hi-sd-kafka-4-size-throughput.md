---
id: hi-sd-kafka-4-size-throughput
node: sd.deep-dives.kafka
type: qa
step: 4
---
## Q
**单 broker 的量级与「别把大文件放 Kafka」**｜系统设计 · 深入技术

一个 Kafka broker 大概能承载多少数据与吞吐？消息大小有什么讲究？视频转码场景该怎么用 Kafka？

## A
**数字。** 好硬件上单 broker 约存 1TB、每秒约 100 万条消息（粗略估算，取决于消息大小与硬件）。需求没超过它，就不必谈扩展。

**消息大小。** 没有硬上限（`message.max.bytes` 可配），但建议小于 1MB，以减少内存压力、提高网络利用率。

**易错。** 把大 blob 放进 Kafka 是常见反模式，它不是数据库。做 YouTube 时不要把视频本体塞进 topic，应把视频存 S3，只在消息里放 S3 位置作为指针，消费者按指针去取。

**说法。** 先估算吞吐和存储，再决定要不要谈扩展。
