---
id: kafka-admin-delete-group-requires-empty
node: admin.consumer-group-ops
type: qa
source: kafka-2e
---
## Q
用 `kafka-consumer-groups.sh --delete` 删除一个消费者群组时，如果群组里还有消费者在运行，会发生什么？

## A
命令会直接失败，并抛出「群组不为空」的异常。删除消费者群组会把这个群组保存的所有已提交偏移量一并删除，所以 Kafka 要求必须先把群组里所有消费者都关闭，确保群组已经清空，才允许执行删除，避免在消费者还依赖这些偏移量的情况下把它们连同群组一起删掉。
