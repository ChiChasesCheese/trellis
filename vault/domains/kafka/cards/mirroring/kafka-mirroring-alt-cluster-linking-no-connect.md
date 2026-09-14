---
id: kafka-mirroring-alt-cluster-linking-no-connect
node: mirroring.alternatives
type: qa
source: kafka-2e
---
## Q
集群链接（cluster linking，Confluent Server 提供的跨集群复制特性）和 MirrorMaker 这类基于 Connect 的外部镜像工具相比，在实现方式和运维复杂度上有什么本质区别，带来了什么运维和性能上的好处？

## A
集群链接不依赖任何外部组件（不需要单独搭建和运维 Connect 集群），而是直接扩展了 Kafka 集群内部原生的 broker 间复制协议，把这套本来只在同一个集群内部用于副本同步的协议直接用在跨集群复制上：目标集群的首领 broker 直接向源集群对应的首领拉取分区数据，目标集群的跟随者再用标准的集群内复制机制从本地首领同步。因为没有中间的 Connect 层做数据的反序列化再序列化，也就避免了外部镜像工具在镜像过程中常见的解压缩、再压缩开销，效率更高；同时因为不需要额外部署和维护一套独立的镜像组件，运维也更简单。目标集群里被镜像过来的主题会被标记为**只读**，防止本地生产者意外写入，从而保证镜像主题在逻辑上和源主题保持一致。
