---
id: hi-c-sd-kafka-n14-summary
node: sd.deep-dives.kafka.notes
type: qa
step: 13
---
## Q
**Kafka · 总结：面试里怎么用**｜摘要 · 必会

一句话怎样概括 Kafka？谈扩展时应该从哪里开始？

## A
- **概括：** 开源的分布式事件流平台，高性能、可扩展、持久。生产者把消息发到主题，消费者读取，消息按有序、不可变的分区存在多个 broker 上，适合实时数据处理和异步消息队列。
- **谈扩展时：** 先讲分区策略，以及怎么处理热点分区。
- **相关的记忆点：** Kafka 默认偏可用，`acks=all` 加 `min.insync.replicas` 时偏一致；消费者故障比 Kafka 本身故障更值得讨论。
