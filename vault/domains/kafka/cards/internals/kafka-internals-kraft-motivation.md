---
id: kafka-internals-kraft-motivation
node: internals.kraft-mode
type: qa
source: kafka-2e
---
## Q
Kafka 社区从 2019 年开始用基于 Raft（一种分布式一致性算法）的 KRaft 控制器取代基于 ZooKeeper（外部协调服务）的传统控制器。抛开「少依赖一个外部系统」，主要的技术性动因有哪些？

## A
主要有三条：1）传统架构下，元数据虽然同步写入 ZooKeeper，但同步给各 broker 以及 broker 从 ZooKeeper 接收更新都是**异步**的，多环节异步容易导致 broker、控制器、ZooKeeper 三者的元数据出现难以检测的不一致；2）控制器重启时要从 ZooKeeper 完整读出所有 broker 和分区的元数据再逐一发给每个 broker，这个过程随分区和 broker 数量增长会越来越慢，是长期存在的瓶颈；3）元数据的归属很混乱——有些操作走控制器、有些走 broker、有些直接改 ZooKeeper，内部架构缺乏统一所有权。这些问题共同限制了 Kafka 能支撑的分区规模。
