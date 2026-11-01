---
id: hi-sd-cap-theorem-1-three-properties
node: qb.sd.distributed-rate-limiter.pre-sd-core-concepts-cap-theorem
type: qa
step: 1
---
## Q
**CAP 三个字母与真正的选择**｜系统设计 · 核心概念

CAP 定理说分布式系统三者只能得其二，三个性质分别指什么？为什么面试里它实际只剩「一致性还是可用性」这一个选择？

## A
**要点。**
- 一致性（Consistency）：某次写入完成后，从任何节点读到的都是这个新值
- 可用性（Availability）：每个没出故障的节点都必须应答，但不保证内容是最新版本
- 分区容错（Partition Tolerance）：节点之间丢消息、断网时系统仍能运转

**为什么。** 网络故障一定会发生，所以分布式系统必须容忍分区，P 不是可选项。「三选二」于是退化成：发生分区时，是保一致性还是保可用性。

**易错。** CAP 里的 C 与 ACID 里的 C（事务不破坏约束）不是一回事，CAP 的 C 说的是各副本读到同一份最新数据。没有分区时，两者可以同时拥有。
