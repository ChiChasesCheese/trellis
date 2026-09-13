---
id: kafka-producer-avro-generic-vs-specific-record
node: producer.serialization
type: qa
source: kafka-2e
---
## Q
用 Avro 发送数据时，「基于模式生成的专用对象（如 Customer 类）」和「通用的 GenericRecord」这两种方式有什么区别？

## A
专用对象是通过 Avro 代码生成工具，根据模式预先生成带有 getter/setter 方法的 Java 类（如 Customer），发送前需要先生成好这些类；GenericRecord 则像一个通用的键值容器（类似 map），可以在运行时直接用一个 Schema 对象和字段名/值来构造记录，不需要事先生成任何专用类。两者最终都通过 KafkaAvroSerializer 序列化，效果一样，区别只在于开发时是否需要预先生成模式对应的类。
