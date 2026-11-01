---
id: hi-sd-cassandra-2-partitioning
node: qb.sd.notification-system-scale.pre-sd-deep-dives-cassandra
type: qa
step: 2
---
## Q
**分区与复制：一致性哈希加虚拟节点**｜系统设计 · 深入专题

Cassandra 怎样把数据分到各节点并做副本？为什么不用 `hash(key) % N`？

## A
**要点。** 一致性哈希（consistent hashing）：键哈希成一个整数（token），落在环上，顺时针找到的第一个节点就负责它。

**为什么。** `% N` 在节点数变化时几乎所有数据都要搬家，并且可能分布不均。环上增删节点只影响相邻节点。再让每台物理机拥有多个虚拟节点（vnode），负载更均匀，也能让大机器多担 vnode。

**复制。** 副本沿环顺时针再取若干个 vnode，同一物理机上的 vnode 会被跳过，避免一台机器宕机损失多个副本。键空间（keyspace）配置策略：生产用 NetworkTopologyStrategy，感知机架与数据中心，副本分散在不同机架、不同机房；SimpleStrategy 只顺时针取，适合测试和简单部署。例：`dc1` 三副本，`dc2` 两副本。
