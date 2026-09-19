---
id: kafka-producer-avro-writer-reader-schema-compatibility
node: producer.serialization
type: qa
step: 4
source: kafka-2e
---
## Q
使用 Avro 时，「写入数据时用的模式」和「读取数据时用的模式」一定要完全相同吗？反序列化器（deserializer）具体需要用到哪个模式？

## A
不需要完全相同，但两者必须相互兼容（Avro 文档定义了具体的兼容性规则）。反序列化时真正需要用到的是写入数据时所用的那份模式，即使它与读取方当前期望的模式版本不一样，也要能拿到当初写入时的模式，才能正确解析出字段，即便某些字段在读取方版本里已经改名或废弃。
