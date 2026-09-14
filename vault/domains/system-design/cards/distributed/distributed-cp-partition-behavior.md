---
id: distributed-cp-partition-behavior
node: distributed.cap
type: qa
---
## Q
A 5-node CP system (e.g. etcd/ZooKeeper) is partitioned 2 | 3. What can each side do, and what would break if the minority side kept serving?

## A
- **Majority side (3)**: elects/keeps a leader and serves both reads and writes — it can still reach quorum.
- **Minority side (2)**: cannot commit writes, and must not serve reads it claims are current; clients there see unavailability.

If the minority also served: **split brain** — two leaders accepting conflicting writes, or the minority returning stale data as authoritative (breaking linearizability). Quorum intersection (any two majorities of 5 share a node) is exactly what prevents two sides from both thinking they're current.

## Q zh
一个 5 节点的 CP 系统（如 etcd/ZooKeeper）被分区成 2 | 3 两部分。每一侧各能做什么？如果少数派那一侧继续对外提供服务会出什么问题？

## A zh
- **多数派一侧（3 个节点）**：选出/维持一个 leader，同时提供读和写服务——它仍然能达到 quorum。
- **少数派一侧（2 个节点）**：无法提交写入，也不能把自己的读当作最新数据提供服务；这一侧的客户端会看到不可用。

如果少数派也继续服务：就会**脑裂（split brain）**——两个 leader 接受相互冲突的写入，或者少数派把陈旧数据当作权威数据返回（破坏线性一致性）。Quorum 相交（5 个节点中任意两个多数派都共享至少一个节点）正是防止两侧同时自认为是最新状态的原因。
