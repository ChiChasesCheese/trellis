---
id: dist-routing-consistent-hash
node: distributed.routing
type: qa
---
## Q
Why use consistent or rendezvous hashing for cache routing instead of `hash(key) % nodeCount`?

## A
Modulo hashing remaps nearly every key when node count changes, causing a fleet-wide cold cache. Consistent and rendezvous hashing move only the keys assigned to added/removed nodes, preserving locality and hit ratio. Rendezvous hashing is simple to compute from a node list; ring hashing uses virtual nodes for weighting and balance. Both still need bounded-load or load-aware escape paths for skew and unhealthy nodes.

## Q zh
cache routing 为什么使用 consistent/rendezvous hashing，而不是 `hash(key) % nodeCount`？

## A zh
modulo hashing 在 node count 变化时几乎重映射全部 key，制造 fleet-wide cold cache。consistent 和 rendezvous hashing 只移动属于新增/删除 node 的 key，保留 locality 与 hit ratio。rendezvous hashing 可从 node list 简单计算；ring hashing 用 virtual node 做 weight 和 balance。两者面对 skew 或 unhealthy node 时，仍需要 bounded-load 或 load-aware escape path。
