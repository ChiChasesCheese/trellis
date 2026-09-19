---
id: kafka-reliability-min-insync-replicas
node: reliability.broker-config
type: qa
step: 3
source: kafka-2e
---
## Q
一个复制系数为 3 的主题把 `min.insync.replicas`（最少同步副本数）设置为 2。如果集群里有 2 个副本同时变得不可用，只剩 1 个同步副本，broker 会怎么处理这时候的生产请求和消费请求？为什么这样设计？

## A
broker 会拒绝生产者的写入请求，抛出 `NotEnoughReplicasException`（同步副本不足异常）；但消费者仍然可以继续读取分区里已有的数据，也就是说这个分区实质上变成了**只读**状态，要等两个不可用副本中至少一个恢复并重新追上同步状态，才能恢复可写。这样做是因为如果只剩 1 个同步副本时还允许写入，一旦这个副本随后也失效，就必须在「数据不可用」和「触发不彻底选举丢数据」之间二选一；`min.insync.replicas=2` 提前把「已提交」的门槛设在至少 2 个副本上，宁可暂停写入也不让数据只依赖单个副本。
