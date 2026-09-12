---
id: kafka-connect-alt-flume-logstash-vs-connect
node: connect.alternatives
type: qa
source: kafka-2e
---
## Q
一个团队的数据架构以 Hadoop 或 ElasticSearch 为中心，Kafka 只是众多数据来源之一；另一个团队的架构以 Kafka 为中心，需要对接大量各种各样的源系统和目标系统。这两种情况分别更适合用 Flume/Logstash 这类系统自带的数据摄入工具，还是用 Kafka Connect？

## A
以 Hadoop 或 ElasticSearch 为中心、Kafka 只是数据来源之一的架构，更适合继续用它们各自生态原生的摄入工具——Hadoop 用 Flume，ElasticSearch 用 Logstash 或 Fluentd，因为整个数据流的核心枢纽本来就不是 Kafka。反过来，如果架构以 Kafka 为核心，需要连接许多不同的源系统和目标系统，用 Connect 更合适，因为 Connect 就是围绕 Kafka 设计的统一集成层，能用同一套连接器机制覆盖多种异构系统，不需要为每种上下游系统单独引入一套摄入工具。
