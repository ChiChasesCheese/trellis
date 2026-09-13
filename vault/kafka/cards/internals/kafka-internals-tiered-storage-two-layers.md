---
id: kafka-internals-tiered-storage-two-layers
node: internals.tiered-storage
type: qa
source: kafka-2e
---
## Q
分层存储（tiered storage，KIP-405）给 Kafka 集群引入了「本地存储层」和「远程存储层」两层。这两层分别用什么介质，各自的保留时间设置通常有什么差异？

## A
本地存储层和以前一样，用 broker 自己的本地磁盘保存日志片段（log segment）；远程存储层则把日志片段存到 HDFS、S3 这类专用的低成本对象存储系统里，两层可以分别配置各自的保留策略。因为本地磁盘的单位存储成本明显高于远程对象存储，本地层的保留时间通常只设几小时甚至更短，远程层则可以设成几天甚至几个月，把「贵的存储」用得少、「便宜的存储」放长期数据。
