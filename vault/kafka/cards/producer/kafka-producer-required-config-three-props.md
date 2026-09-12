---
id: kafka-producer-required-config-three-props
node: producer.client-basics
type: qa
source: kafka-2e
---
## Q
创建一个 Kafka 生产者（producer，向 Kafka 写入消息的客户端）对象时，有哪三个属性是必须设置的？各自的作用是什么？

## A
必须设置：`bootstrap.servers`（一组 broker 的 host:port 地址，用于建立到集群的初始连接）、`key.serializer`（把消息的键序列化成字节数组的类）、`value.serializer`（把消息的值序列化成字节数组的类）。之所以键和值的序列化器都要配置，是因为 broker 只接受字节数组；即使应用只关心值、不使用键，也必须显式给 key.serializer 配一个类型（如 VoidSerializer）。
