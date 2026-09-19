---
id: kafka-admin-force-move-controller
node: admin.partition-reassignment
type: qa
step: 5
source: kafka-2e
---
## Q
Kafka 集群的控制器（controller，负责监督分区状态变更等集群级操作的特殊 broker 角色）出现异常但主机进程还在运行、没有真正宕机，导致集群操作不正常时，如何在不关闭这台机器的情况下强制把控制器角色转移给别的 broker？

## A
正常情况下控制器角色是通过在 ZooKeeper 上抢占一个临时节点 `/admin/controller` 来选举产生的，控制器所在 broker 一旦断开连接，这个临时节点会被自动删除，其他 broker 就会去竞争成为新控制器。要在不关闭这台主机的情况下强制换控制器，可以手动删除这个 `/admin/controller` 节点，让当前控制器主动退出控制器角色，集群会随机选出一个新的控制器；不过目前 Kafka 不支持直接指定「换成哪个 broker」当控制器。这个操作通常风险不高，但仍属于非常规操作，不应该经常使用。
