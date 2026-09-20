---
id: kafka-internals-kraft-metadata-as-log
node: internals.kraft-mode
type: qa
step: 2
source: kafka-2e
---
## Q
KRaft（基于 Raft 的新控制器架构）用什么方式取代了 ZooKeeper 原来保存集群元数据（主题、分区、ISR、配置等）的角色？为什么选这种方式？

## A
KRaft 把集群元数据的每一次变更都表示成一个事件，写进一份由控制器节点共同维护的**元数据事件日志**——这正是 Kafka 本身最擅长的「基于日志的架构」：状态变化被表示成一串有序事件流，任何一方都可以通过重放（replay）这份日志追上最新状态。原来保存在 ZooKeeper 里的一切都被搬进了这份日志，好处是元数据的表示方式和 Kafka 自身的数据模型统一了，社区对「重放事件得到最新状态」这种模式也非常熟悉，容易推理和维护。
