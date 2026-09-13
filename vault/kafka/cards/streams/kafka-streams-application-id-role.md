---
id: kafka-streams-application-id-role
node: streams.streams-api
type: qa
source: kafka-2e
---
## Q
创建 KafkaStreams 应用时必须配置 `StreamsConfig.APPLICATION_ID_CONFIG`（应用程序 ID），这个 ID 起什么作用？为什么它必须在同一个 Kafka 集群内保持唯一？

## A
应用程序 ID 有两个作用：一是被同一个应用启动的多个实例用来互相协调、组成一个处理集群（类似消费者群组的机制）；二是被 Streams 用来给这个应用内部自动创建的本地状态存储和相关的内部主题（比如状态变更日志主题）命名。如果同一个 Kafka 集群里两个不同的 Streams 应用用了相同的应用程序 ID，它们各自的实例会被错误地当成同一个应用的不同实例来协调，各自的内部状态存储和内部主题的命名也会互相冲突，导致处理逻辑和状态被搞乱，所以这个 ID 在集群内必须保持唯一。
