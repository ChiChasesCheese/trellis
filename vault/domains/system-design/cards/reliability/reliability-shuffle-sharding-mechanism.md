---
id: reliability-shuffle-sharding-mechanism
node: reliability.resilience.containment
type: qa
---
## Q
What is shuffle sharding, and why does giving each customer a random 2-node subset of an 8-node fleet contain a poison-pill client far better than splitting the fleet into fixed shards?

## A
- **Plain sharding**: split 8 nodes into 4 fixed shards of 2 and pin each customer to one shard. A **poison-pill client** (a request that crashes or saturates whatever serves it — a targeted DDoS, a pathological query) takes down its shard, and **every** customer on that shard suffers total outage: blast radius 1/4 of customers at 100% impact.
- **Shuffle sharding**: assign each customer their own *random combination* of 2 nodes (a "virtual shard"). The bad client still kills its own 2 nodes, but only customers assigned **exactly the same pair** lose both — most overlapping customers share just **one** node, and their requests succeed on their other node via retries.
- So blast radius shrinks from 1/(number of shards) to roughly 1/(number of *combinations*), using the same hardware — the isolation comes from combinatorics, not from buying more nodes. The catch: clients (or the routing layer) must actually retry across their shard members, or partial overlap gives no protection.

## Q zh
什么是 shuffle sharding？为什么给每个客户随机分配 8 节点集群中的 2 个节点，比把集群切成固定 shard 更能遏制 poison-pill 客户端？

## A zh
- **普通 sharding**：把 8 个节点切成 4 个固定的 2 节点 shard，每个客户钉在一个 shard 上。一个 **poison-pill 客户端**（能打垮任何服务它的节点的请求 — 定向 DDoS、病态查询）会打垮它所在的 shard，该 shard 上的**每个**客户都全量中断：爆炸半径是 1/4 的客户、100% 的影响。
- **Shuffle sharding**：给每个客户分配自己的*随机组合*——2 个节点（一个"虚拟 shard"）。坏客户端仍然打垮自己那 2 个节点，但只有被分到**完全相同一对节点**的客户才会两个都失去 — 大多数有重叠的客户只共享**一个**节点，重试后请求在另一个节点上成功。
- 于是爆炸半径从 1/(shard 数) 缩小到约 1/(组合数)，硬件不变 — 隔离来自组合数学，不是买更多节点。前提：客户端（或路由层）必须真的在自己 shard 的成员间重试，否则部分重叠不提供任何保护。
