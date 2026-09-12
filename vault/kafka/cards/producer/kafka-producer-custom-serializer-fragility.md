---
id: kafka-producer-custom-serializer-fragility
node: producer.serialization
type: qa
source: kafka-2e
---
## Q
为什么不建议给业务对象手写自定义序列化器（custom serializer），而是推荐使用 Avro、Thrift、Protobuf 这类通用序列化框架？

## A
手写序列化器把字段的编码方式硬编码在代码里，一旦对象结构发生变化（比如把某个字段类型从 int 改成 long，或新增一个字段），新旧序列化器产生的字节数组就不兼容，排查这种兼容性问题需要直接比较原始字节，非常困难。而且如果公司里多个团队都要写入同一种对象，大家必须使用完全相同的序列化器代码并同步修改，协调成本很高。通用序列化框架把模式和序列化逻辑分离，能更好地处理这些问题。
