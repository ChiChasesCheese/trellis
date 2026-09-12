---
id: kafka-core-replication-scoped-to-single-cluster
node: core.cluster-roles
type: qa
source: kafka-2e
---
## Q
如果业务同时运行在多个数据中心、需要用到多个 Kafka 集群，能不能依靠 Kafka 内置的分区复制机制（replication）把数据从一个集群复制到另一个集群？

## A
不能。Kafka 的分区复制机制只能在单个集群内部把数据复制到不同的 broker 上（用于容错），不支持跨集群复制。要在多个集群之间同步数据，需要使用专门的工具（如 MirrorMaker），不能依赖普通的副本机制。
