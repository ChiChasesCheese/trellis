---
id: kafka-consumer-seek-changes-poll-position-not-commit
node: consumer.seek-and-replay
type: qa
source: kafka-2e
---
## Q
调用 `consumer.seek(partition, offset)` 之后，下一次调用 `poll()` 会从哪里开始读取？这个操作本身会不会顺带把这个新位置提交到 Kafka？

## A
`seek()` 只是修改了消费者在内存里对这个分区「下一次要读取的位置」，之后紧接着的 `poll()` 就会从这个新设置的偏移量开始返回消息。但 `seek()` 本身并不会自动提交偏移量——是否要把这个新位置持久化为已提交偏移量，仍然需要应用程序自己显式调用提交方法，否则一旦发生再均衡或消费者重启，进度又会退回到上一次真正提交过的偏移量。
