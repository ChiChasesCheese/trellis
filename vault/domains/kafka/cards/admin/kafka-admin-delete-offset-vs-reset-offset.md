---
id: kafka-admin-delete-offset-vs-reset-offset
node: admin.consumer-group-ops
type: qa
step: 4
source: kafka-2e
---
## Q
想让一个消费者群组（consumer group，共同分摊读取同一批分区的一组消费者）重新从主题最开始的位置读取数据，为什么直接「删除」它已提交的偏移量（offset，消费者在某个分区里读到的位置）不是可靠的做法，而应该显式把偏移量「重置」为最早的偏移量？

## A
删除偏移量只是让消费者在下次启动时找不到已提交的位置，此时它到底从最早位置开始读，还是直接跳到最新位置开始读，完全取决于消费者自身的 `auto.offset.reset` 配置——如果这个消费者配置的是跳到最新位置，删除偏移量反而会让它跳过所有历史数据。要保证消费者一定从头开始读，必须显式地把提交的偏移量改写成这个分区最早的偏移量（用 `OffsetSpec.earliest()` 查到后写回去），这样不管 `auto.offset.reset` 配了什么，消费者启动时读到的都是明确指定的最早位置。
