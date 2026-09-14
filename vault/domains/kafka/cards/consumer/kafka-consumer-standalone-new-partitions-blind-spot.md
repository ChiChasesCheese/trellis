---
id: kafka-consumer-standalone-new-partitions-blind-spot
node: consumer.standalone
type: qa
source: kafka-2e
---
## Q
使用 `assign()` 给独立消费者指定分区之后，如果这个主题后来被管理员增加了新分区，消费者会自动感知并开始读取新分区吗？需要怎么处理？

## A
不会自动感知。独立消费者用 `assign()` 手动指定的分区列表是固定的，Kafka 不会像消费者群组那样在主题变化时主动通知它、触发重新分配。要跟上新增的分区，需要应用程序自己定期调用 `consumer.partitionsFor()` 检查是否有新分区出现，或者干脆约定每次给主题加分区之后就重启一次这个独立消费者应用。
