---
id: kafka-consumer-seektobeginning-seektoend-purpose
node: consumer.seek-and-replay
type: qa
source: kafka-2e
---
## Q
如果想让消费者跳过所有历史积压消息、只读之后新产生的数据，或者反过来想重新处理某个分区从头到尾的全部历史消息，应该调用哪两个 API？

## A
调用 `consumer.seekToEnd(partitions)` 可以把消费者在指定分区上的读取位置直接跳到分区末尾，之后 `poll()` 就只会返回跳转之后新写入的消息，用于跳过大量积压数据；调用 `consumer.seekToBeginning(partitions)` 则会把位置重置到分区起始处，让消费者从头开始重新读取该分区里所有仍然保留着的历史消息，用于完整重放。
