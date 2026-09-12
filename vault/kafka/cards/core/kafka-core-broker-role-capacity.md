---
id: kafka-core-broker-role-capacity
node: core.cluster-roles
type: qa
source: kafka-2e
---
## Q
在 Kafka 集群里，「broker」具体指什么？它承担哪些职责？

## A
一个 broker 就是一台独立运行的 Kafka 服务器。它接收生产者发来的消息，为消息分配偏移量（offset）并提交到磁盘保存；同时响应消费者的读取请求，把已发布的消息返回给它们。根据硬件配置不同，单个 broker 可以轻松处理数千个分区、每秒百万级的消息量，是 Kafka 存储和服务能力的基本单位。
