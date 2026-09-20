---
id: kafka-consumer-avro-specific-reader-config
node: consumer.deserialization
type: qa
step: 4
source: kafka-2e
---
## Q
消费者用 `KafkaAvroDeserializer` 反序列化 Avro 消息时，配置 `specific.avro.reader=true` 起什么作用？

## A
它告诉反序列化器把消息还原成代码生成工具预先生成的「专用」Avro 类实例（比如带有 getName()、getID() 这类方法的 Customer 类），而不是还原成通用的 GenericRecord（类似 map 的通用容器）。这样消费者代码就能用生成类的强类型访问方式来读取字段，而不用像操作 GenericRecord 那样通过字段名去取值。
