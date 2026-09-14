---
id: datastream-vs-connector-plus-streaming
node: ingestion.datastream-kafka-compatible
type: qa
tags: [grown]
---
## Q
把 Kafka 数据导入 Snowflake，传统做法是「自建 Kafka 集群 + Snowflake Kafka Connector（底层用 Snowpipe Streaming）」。Datastream 在架构上省掉了什么？

## A
传统做法里，Kafka 集群和连接器进程都是要单独部署、扩容、监控的基础设施，数据先进入 Kafka 再被连接器搬进表。Datastream 让生产者直接用 Kafka 协议写入 Snowflake 原生服务，主题直接落地为表，省去了独立的 Kafka 集群和中间搬运层，流式数据与分析数据处于同一个平台之内。
