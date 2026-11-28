---
id: hi-c-sd-zookeeper-b04-kraft
node: sd.deep-dives.zookeeper.beyond
type: qa
step: 4
---
## Q
**ZooKeeper · 从 ZooKeeper 到 KRaft：为什么内置共识更好**｜拓展 · 加分

Kafka 为什么要抛弃 ZooKeeper？内置共识具体改善了什么？

## A
- **两套系统的负担：** 以前运维 Kafka 还要运维一套 ZooKeeper，两套安全、监控、升级。集群的元数据存在 ZooKeeper 里，控制器要先从 ZooKeeper 把所有元数据读出来，分区越多恢复越慢。
- **KRaft 做法：** 元数据本身是 Kafka 内部的一个用 Raft 复制的日志，由一组控制器节点管理，活动控制器随时在内存里持有最新元数据，故障切换时备用控制器已经基本追平。
- **得到的好处：** 少一个系统要部署；控制器故障恢复更快；可以支持更多分区；元数据变更以事件日志的形式传播给 broker，而不是靠 broker 各自拉取。
- **进展：** 新版本（Kafka 4.0）已不再支持 ZooKeeper 模式，老集群需要迁移。
- **2026 亮点：** 4.0 起只有 KRaft：元数据由 controller quorum 用 Raft 复制，broker 要求 Java 17；还在 ZooKeeper 模式的老集群必须先迁到 KRaft 才能升 4.x（3.9 是最后带迁移功能的版本，并支持动态调整 controller quorum，KIP-853）。别再画“Kafka + ZooKeeper”的架构图。
- **泛化的教训：** 当一个系统的核心状态已经需要共识时，把共识内置通常比依赖外部协调服务更简单可靠。
