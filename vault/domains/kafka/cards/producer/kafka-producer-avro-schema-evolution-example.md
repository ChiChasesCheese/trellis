---
id: kafka-producer-avro-schema-evolution-example
node: producer.serialization
type: qa
step: 5
source: kafka-2e
---
## Q
一个 Avro 模式（schema，描述消息结构的规范）原本有 `faxNumber` 这个可选字段，后来被替换成 `email` 字段。还在用旧代码的消费者程序，读到用新模式写的消息时会发生什么？为什么不会报错中断？

## A
消费者程序调用 `getFaxNumber()` 读取传真号字段时会得到 null，因为新消息里根本没有这个字段，但整个反序列化过程不会抛异常、也不会中断。这是 Avro 模式演化（schema evolution）的效果：只要新旧模式相互兼容，读取方即使还没升级到能识别新字段（如 `getEmail()`）的版本，依然能正常处理消息，只是取不到新字段的值。
