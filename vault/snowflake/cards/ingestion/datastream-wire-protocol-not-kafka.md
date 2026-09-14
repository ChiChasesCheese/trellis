---
id: datastream-wire-protocol-not-kafka
node: ingestion.datastream-kafka-compatible
type: qa
tags: [grown]
---
## Q
Snowflake Datastream 号称「兼容 Kafka」。它是在 Snowflake 里托管了一套 Apache Kafka 集群吗？「兼容」具体指什么？

## A
不是。Datastream 是 Snowflake 自研的全托管流式服务，底层并不运行 Kafka，只是实现了 Kafka 线上协议（wire protocol，客户端与 broker 之间通信的二进制协议）。因此现有的 Kafka 生产者和消费者只需把连接地址等配置指向 Datastream，无需改写代码，而数据落地为受治理的 Snowflake 表或 Apache Iceberg 表。
