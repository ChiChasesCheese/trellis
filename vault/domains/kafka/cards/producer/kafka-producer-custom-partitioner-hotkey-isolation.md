---
id: kafka-producer-custom-partitioner-hotkey-isolation
node: producer.extensibility
type: qa
step: 3
source: kafka-2e
---
## Q
一个 B2B 供应商的某个大客户贡献了超过10%的交易量。如果继续用默认的哈希分区策略，会带来什么问题？自定义分区器（custom partitioner）如何解决它？

## A
默认哈希分区器会把这个大客户的消息和其他客户的消息混在同一个（由哈希值决定的）分区里，导致这个分区的数据量远大于其他分区，可能造成该分区所在服务器存储紧张、请求处理变慢。解决办法是实现 Kafka 的 Partitioner 接口，在 partition() 方法里对这个大客户的键做特殊判断（比如固定分配到某个专用分区），其余客户的消息仍按哈希算法分配到剩下的分区，从而把热点客户的负载单独隔离开。
