---
id: kafka-internals-tiered-storage-decouple-storage-compute
node: internals.tiered-storage
type: qa
source: kafka-2e
---
## Q
分层存储让 Kafka 集群「延长数据保留时间」这件事不再需要「扩大集群」，具体是通过什么方式实现存储与计算（CPU/内存）的解耦，还带来了哪些附加好处？

## A
远程存储层用的是 HDFS、S3 这类可以独立于 broker 计算资源扩展的专用存储系统，所以要延长整体数据保留期只需要在远程层多存数据，不需要给 broker 加磁盘或加节点，实现了存储容量扩展与 CPU/内存扩展的解耦。附加好处还有：留在 broker 本地的数据量变小，故障恢复和再均衡（rebalance）时需要在 broker 间复制的数据量也随之减少（远程存储里的片段不需要恢复到 broker 本地，除非按需读取）；此外也不再需要像以前那样另外搭一条独立的数据管道把数据从 Kafka 复制到外部存储系统来实现长期保留。
