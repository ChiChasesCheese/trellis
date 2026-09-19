---
id: kafka-producer-idempotence-solves-ordering
node: producer.idempotence-ordering
type: qa
step: 4
source: kafka-2e
---
## Q
如果既想让 `max.in.flight.requests.per.connection`（生产者在收到响应前能连续发送的批次数）大于1以提升吞吐量，又想开启重试以提升可靠性，但又担心重试打乱消息顺序，解决方案是什么？

## A
把 `enable.idempotence` 设置为 true。开启幂等生产者后，Kafka 在最多允许 5 个请求同时在途的情况下仍然能保证消息顺序不被打乱，同时借助序列号机制保证重试不会引入重复消息，这样就同时兼顾了并发在途请求带来的吞吐量、以及顺序和不重复这两个可靠性要求，不需要再在它们之间做取舍。
