---
id: distributed-consensus-in-practice
node: distributed.consensus
type: qa
---
## Q
Where does consensus actually sit in production architectures, and why don't you run your main data path through it?

## A
It sits in the **control plane**, on small state: leader election, cluster membership, shard→node maps, distributed locks, config — via etcd/ZooKeeper (Kubernetes, Kafka's KRaft), or per-shard Raft groups replicating a WAL (CockroachDB, TiDB, Kafka partitions).

You keep bulk data off a single consensus group because every write pays a **quorum round-trip and one leader's throughput cap** — it doesn't scale horizontally; you scale by running **many independent Raft groups** (one per shard/partition). Interview phrasing: "consensus for coordination and metadata; replication + partitioning for data, often consensus-per-shard."

## Q zh
共识在实际的生产架构中到底处于什么位置？为什么你不会让主数据路径经过它？

## A zh
它位于**控制平面**，处理的是很小的状态：领导者选举、集群成员关系、分片→节点映射、分布式锁、配置——通过 etcd/ZooKeeper（Kubernetes、Kafka 的 KRaft），或者按分片划分的 Raft 组来复制 WAL（CockroachDB、TiDB、Kafka 分区）。

之所以让大批量数据远离单一的共识组，是因为每次写入都要付出**一次 quorum 往返以及单个 leader 的吞吐上限**——它无法水平扩展；要扩展就得运行**许多相互独立的 Raft 组**（每个分片/分区一个）。面试表述："共识用于协调和元数据；复制 + 分区用于数据，而且往往是按分片各自共识。"
