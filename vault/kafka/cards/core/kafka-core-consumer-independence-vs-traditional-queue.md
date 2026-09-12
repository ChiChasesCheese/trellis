---
id: kafka-core-consumer-independence-vs-traditional-queue
node: core.pubsub-why
type: qa
source: kafka-2e
---
## Q
在传统消息队列系统中，一条消息一旦被某个客户端读取，其他客户端就再也读不到它了。Kafka 的多消费者模型与此有何不同？

## A
Kafka 允许多个消费者（consumer）各自独立地从同一个消息流读取数据，彼此互不影响：某个消费者读取了一条消息，并不会让这条消息对其他消费者「消失」。这与传统队列里消息一旦被拿走即失效、只能被一个客户端消费的语义不同，任何订阅了该主题的消费者都能各自按自己的进度读取到全部消息。
