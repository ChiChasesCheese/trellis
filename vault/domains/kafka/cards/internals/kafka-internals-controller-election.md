---
id: kafka-internals-controller-election
node: internals.controller
type: qa
step: 2
source: kafka-2e
---
## Q
一个 Kafka 集群刚启动，或者当前控制器（controller，负责首领选举的那个 broker）突然下线了。集群是如何选出（新）控制器的？为什么这种方式能保证同一时刻只有一个控制器？

## A
Kafka 依赖 ZooKeeper 里一个固定路径 `/controller` 的**临时节点（ephemeral node）**：临时节点会随创建它的客户端连接断开而自动消失。集群中第一个成功在 `/controller` 创建该节点的 broker 就成为控制器；其余 broker 尝试创建时都会收到「节点已存在」的异常，从而知道控制器已经产生，转而在这个节点上注册 ZooKeeper watch（监听变更的订阅）。因为 ZooKeeper 保证同一路径的临时节点在同一时刻只能被一个客户端持有，所以「谁先创建成功」天然是唯一的，不会出现两个 broker 同时自认为是控制器的情况。当控制器下线或与 ZooKeeper 断开（例如超过 `zookeeper.session.timeout.ms` 未发心跳），节点消失，其余 broker 收到 watch 通知后重新抢占创建，重复上述过程选出新控制器。
