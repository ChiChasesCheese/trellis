---
id: kafka-producer-idempotence-duplicate-scenario
node: producer.idempotence-ordering
type: qa
step: 1
source: kafka-2e
---
## Q
即使把 `acks` 设为 all 并加大重试次数以追求可靠性，为什么消息仍有可能被写入 Kafka 不止一次？

## A
设想一个 broker 收到消息，写入本地磁盘并成功复制给了其他副本，但还没来得及把成功响应发回给生产者就崩溃了。生产者等不到响应，达到 `request.timeout.ms` 后判断这次请求失败，于是重试，把同一条消息发给了新首领；但新首领其实已经通过复制拿到了这条消息，于是这条消息就在分区里出现了两次。也就是说，`acks=all` 加重试只能保证「至少写入一次」，不能保证「只写入一次」。
