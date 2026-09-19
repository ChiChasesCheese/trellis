---
id: kafka-consumer-custom-deserializer-tight-coupling
node: consumer.deserialization
type: qa
step: 2
source: kafka-2e
---
## Q
为什么不建议使用自定义反序列化器（custom deserializer），即使它的写法并不复杂？

## A
自定义反序列化器要求消费者端使用和生产者端完全对应的类定义和字节布局逻辑（比如同一个 Customer 类），一旦生产者那边修改了对象结构，所有使用自定义反序列化器的消费者代码都要跟着同步修改，这把生产者和消费者紧紧耦合在一起，在有多个团队共享同一份数据的大企业里很容易出错、难以协调。推荐改用 JSON、Thrift、Protobuf 或 Avro 这类标准的消息格式来代替手写的序列化器/反序列化器。
