---
id: kafka-producer-delivery-timeout-vs-request-timeout
node: producer.timeouts-retries
type: qa
step: 1
source: kafka-2e
---
## Q
`delivery.timeout.ms` 和 `request.timeout.ms` 都是「超时」参数，二者控制的时间范围有什么不同？

## A
`request.timeout.ms` 只控制生产者在放弃单次请求之前，等待 broker 对这一次请求作出响应的时间，不包含重试和发送前排队的时间。`delivery.timeout.ms` 覆盖的范围更大：从消息准备好被发送（放入批次）开始，一直到 broker 最终响应或生产者放弃全部重试为止的总时间，所以它的值必须大于 `linger.ms` 加 `request.timeout.ms`，否则会抛出异常。
