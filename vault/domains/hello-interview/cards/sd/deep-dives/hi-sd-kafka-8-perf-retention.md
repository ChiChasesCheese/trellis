---
id: hi-sd-kafka-8-perf-retention
node: sd.deep-dives.kafka
type: qa
step: 8
---
## Q
**性能优化与保留策略**｜系统设计 · 深入技术

提升 Kafka 吞吐有哪些手段？消息默认保留多久，需要保留更久怎么办？

## A
**手段。**
- 批量发送：生产者本就会攒批，减少网络开销
- 压缩：支持 GZIP、Snappy、LZ4，消息变小传得更快
- 分区键：影响最大的是分区键，要让消息在分区间均匀，最大化并行度

**保留策略。** 由 `retention.ms` 与 `retention.bytes` 控制，默认保留 7 天。需要更久，可调长，但要考虑存储成本与性能。

**取舍。** 保留越久，重放能力越强，磁盘越贵。

**说法。** 使用托管服务（Confluent Cloud、AWS MSK）时许多扩展由服务代劳，但面试里仍要讲清底层原理。
