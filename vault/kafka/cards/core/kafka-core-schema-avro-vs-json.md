---
id: kafka-core-schema-avro-vs-json
node: core.topics-partitions
type: qa
source: kafka-2e
---
## Q
Kafka 里的消息只是无结构的字节数组。如果生产者和消费者之间没有约定好的模式（schema，描述消息内容结构的规范），会带来什么问题？为什么很多 Kafka 用户选择 Apache Avro 而不是 JSON/XML？

## A
没有共同模式时，消息的读写会紧密耦合：发布者一改格式，所有订阅者都得先升级才能兼容，反过来也一样，格式演进很脆弱。JSON、XML 这类模式简单易读，但缺乏强类型检查、版本兼容性差。Avro 把模式和消息体分开存储，格式紧凑，并同时支持向前和向后兼容的模式演化（schema evolution）——模式变化时读写双方都不需要重新生成代码，从而解除了读写操作之间的耦合。
