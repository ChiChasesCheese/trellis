---
id: kafka-consumer-required-config
node: consumer.client-basics
type: qa
step: 1
source: kafka-2e
---
## Q
创建一个 KafkaConsumer 对象至少需要设置哪三个属性？另外一个虽非严格必须、但几乎总会用到的第四个属性是什么？

## A
必须设置 `bootstrap.servers`（连接 Kafka 集群的地址列表，作用同生产者）、`key.deserializer` 和 `value.deserializer`（分别把字节数组还原成键和值的 Java 对象，与生产者的序列化器相对应）。此外，`group.id` 虽然严格来说不是必需的（也可以创建不属于任何消费者群组的消费者），但绝大多数场景都会设置它，用来指定这个消费者属于哪一个消费者群组。
