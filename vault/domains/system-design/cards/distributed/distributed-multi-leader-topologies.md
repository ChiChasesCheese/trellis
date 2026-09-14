---
id: distributed-multi-leader-topologies
node: distributed.replication.multi-leader
type: qa
---
## Q
Circular, star, and all-to-all multi-leader topologies — what does each risk, and what extra metadata does every one of them need?

## A
- **Circular / star**: each write forwards along a fixed path. One node down **breaks the chain** until reconfigured, and every write pays multiple hops. MySQL's classic ring replication is this.
- **All-to-all**: every leader ships to every other. No single-node chokepoint, but messages can **overtake each other** — an `UPDATE` can arrive at a leader before the `INSERT` it depends on, and naive timestamps won't order them.

All topologies need a **replication path tag** on each write (list of node ids it has passed through) so a leader drops writes it has already applied and the write stops circulating. All-to-all additionally needs **causal ordering** — version vectors, not wall clocks — which is exactly the bug most hand-rolled multi-master setups ship with.

## Q zh
环形、星形和全连接三种多主拓扑——各自的风险是什么？每一种都需要额外携带什么元数据？

## A zh
- **环形 / 星形**：每次写沿固定路径转发。一个节点宕机就会**打断链条**，直到重新配置，而且每次写都要付出多跳的代价。MySQL 经典的环形复制就是这种。
- **全连接**：每个 leader 向所有其他 leader 发送。没有单点瓶颈，但消息可能**互相超车**——一个 `UPDATE` 可能在它依赖的 `INSERT` 之前到达某个 leader，朴素的时间戳无法给它们排序。

所有拓扑都需要在每次写上带一个**复制路径标签**（它经过的节点 id 列表），这样一个 leader 才能丢弃自己已经应用过的写、让写停止循环传播。全连接还额外需要**因果排序**——用版本向量，而不是墙钟——这正是大多数手搓的多主方案会踩的坑。
