---
id: problems-key-value-store-10x-node-growth
node: problems.foundations.key-value-store
type: qa
step: 8
tags: [grown]
---
## Q
In a Dynamo-style key-value store designed for 300M monthly active users at ~167 physical nodes (2,672 virtual nodes at 16 per physical node), what changes mechanically at 10x scale (3 billion MAU), and what does NOT need to change?

## A
Peak QPS grows from ~555,556 to ~5,555,556, and physical node count grows proportionally from ~167 to ~1,667 (virtual nodes to ~26,672 at the same 16-per-node ratio). The consistent-hashing ring routing and gossip-based membership mechanisms don't need to change in kind — gossip convergence only grows from ~8 to ~11 rounds (log2 scaling). What does grow disproportionately is Merkle tree rebuild cost and hinted-handoff queue buildup as node count rises, which pushes toward hierarchical gossip (converging locally within a rack/AZ before syncing across them) to bound cross-domain traffic.

## Q zh
在一个为 3 亿月活设计、约 167 台物理节点（每节点 16 个虚拟节点，共 2,672 个）的 Dynamo 风格键值存储中，扩大到 10 倍规模（30 亿月活）时机制上会发生什么变化？什么不需要变？

## A zh
峰值 QPS 从约 555,556 增长到约 5,555,556，物理节点数相应从约 167 增长到约 1,667（按同样每节点 16 个的比例，虚拟节点增长到约 26,672 个）。一致性哈希环的路由和基于 gossip 的成员管理机制本身不需要发生质变——gossip 收敛只从约 8 轮增长到约 11 轮（对数级扩展）。不成比例增长的是 Merkle 树重建成本和 hinted handoff 队列随节点数上升而产生的积压，这会推动引入分层 gossip（先在机架/可用区内局部收敛，再跨域同步）来约束跨域流量。
