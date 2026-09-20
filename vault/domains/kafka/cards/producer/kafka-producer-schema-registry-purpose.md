---
id: kafka-producer-schema-registry-purpose
node: producer.serialization
type: qa
step: 2
source: kafka-2e
---
## Q
如果每条 Avro 消息都完整携带自己的模式定义，会有什么问题？Kafka 生态里常用什么方案来避免这个问题？

## A
Avro 的完整模式定义体积不小，如果每条消息都内嵌一份完整模式，会成倍增加每条消息的大小，造成很大的存储和网络开销。常见做法是引入一个独立的模式注册表（schema registry，例如 Confluent Schema Registry），把所有用到的模式集中保存在注册表里，消息本身只携带一个模式标识符；生产者写入时把模式注册进去，消费者读取时用这个标识符去注册表里拉取对应的完整模式来反序列化。
