---
id: hi-c-sd-kafka-n12-performance
node: sd.deep-dives.kafka.notes
type: qa
step: 11
---
## Q
**Kafka · 性能优化：批量、压缩、分区键**｜摘要 · 必会

提高 Kafka 吞吐有哪些手段？哪一项影响最大？

## A
- **批处理：** 一次 `send()` 发多条消息；生产者本来就会在发送前把消息攒批以减少开销。`sendBatch()` 可以一次向多个主题发送。
- **压缩：** 设置压缩选项（GZIP、Snappy、LZ4），消息变小，传输更快。
- **影响最大的是分区键：** 目标是让消息均匀分布到各个分区，最大化并行度。面试里谈分区策略几乎总是该最先开口的部分。
