---
id: kafka-consumer-avro-deserializer-early-error-detection
node: consumer.deserialization
type: qa
step: 3
source: kafka-2e
---
## Q
使用 Avro 加模式注册表（schema registry）来做序列化和反序列化，相比自定义反序列化器，在「排查兼容性错误」这件事上有什么明显优势？

## A
AvroSerializer 在生产者写入时就会保证数据与主题的模式兼容，消费者这边任何因为模式不兼容而产生的错误，都会被 Avro 相关的序列化/反序列化组件直接捕获，并附带描述性的错误信息；这样开发者不需要像使用自定义反序列化器那样，在出问题时去逐字节比对、费力调试原始字节数组，问题能更早、更清楚地被发现。
