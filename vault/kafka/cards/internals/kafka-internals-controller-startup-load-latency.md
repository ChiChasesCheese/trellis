---
id: kafka-internals-controller-startup-load-latency
node: internals.controller
type: qa
source: kafka-2e
---
## Q
为什么一个分区数很多的 Kafka 集群里，新控制器（controller）当选后往往需要几秒钟才能真正开始工作，而不是瞬间完成？

## A
新控制器上任后必须先从 ZooKeeper 加载全部主题、分区、副本集的最新状态，之后才能开始管理元数据和执行首领选举。这个加载调用的是异步 API，请求会以「流水线（pipeline）」方式连续发出而不是一条条等待应答，以尽量压低总耗时；但分区数越多，需要拉取和处理的状态越多，所以在分区规模很大的集群里，即便有流水线优化，加载过程仍可能要花上几秒钟。这也是后来 Kafka 社区用基于 Raft 的新控制器（KRaft）取代 ZooKeeper 控制器的动机之一：传统架构下重启控制器的元数据加载会随分区数增长而明显变慢。
