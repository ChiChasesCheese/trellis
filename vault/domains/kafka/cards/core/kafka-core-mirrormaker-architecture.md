---
id: kafka-core-mirrormaker-architecture
node: core.cluster-roles
type: qa
step: 5
source: kafka-2e
---
## Q
Kafka 提供的 MirrorMaker 工具是如何把一个集群的数据复制到另一个集群的？它的核心组件是什么？

## A
MirrorMaker 的核心是一对通过队列相连的消费者和生产者：消费者从源集群读取消息，生产者再把这些消息写入目标集群。典型用法是先把多个「本地」集群的数据汇聚到一个「聚合」集群，再把聚合集群的数据复制到其他数据中心，以此实现跨数据中心的数据同步，弥补 Kafka 副本机制无法跨集群工作的限制。
