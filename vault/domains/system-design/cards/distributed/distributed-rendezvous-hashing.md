---
id: distributed-rendezvous-hashing
node: distributed.partitioning.schemes
type: qa
---
## Q
Rendezvous (highest-random-weight) hashing vs a consistent-hashing ring — how does it work, and when is it the better pick?

## A
For a key, compute `hash(key, node)` for **every** node and pick the node with the highest score; for k replicas, take the top k. Membership change moves only the keys whose winner disappeared — the same minimal-disruption property as a ring, with **no tokens, no vnodes, and no ring state to distribute**. Weighting is a simple per-node multiplier on the score.

Prefer it when:

- The node set is **small and known to every client** (cache tiers, load balancers, shard maps of tens of nodes) — lookup is O(n) per key, which only hurts at large n (cacheable, or use its logarithmic variants).
- You need **ordered replica selection** or per-node weights without hand-tuning token counts.

Prefer the ring when node counts are large or the map must be gossiped incrementally. Related cousin: **Maglev hashing**, which builds a lookup table for O(1) hits and near-perfect balance, used for L4 load balancing.

## Q zh
会合哈希（rendezvous / highest-random-weight hashing）和一致性哈希环相比——它是怎么工作的？什么时候它是更好的选择？

## A zh
对一个 key，为**每一个**节点计算 `hash(key, node)`，选出得分最高的节点；要 k 个副本就取得分最高的前 k 个。成员变化时只有那些"赢家消失了"的 key 会移动——和环一样具有最小扰动的性质，但**不需要 token，不需要虚拟节点，也不需要分发任何环状态**。加权只是在得分上乘一个每节点的系数。

更适合用它的场景：

- 节点集合**小、且所有客户端都知道**（缓存层、负载均衡器、几十个节点的分片映射）——每个 key 的查找是 O(n) 的，只有在 n 很大时才会吃亏（可以缓存，或使用它的对数复杂度变种）。
- 你需要**有序的副本选择**，或者不想手工调 token 数量就能实现按节点加权。

节点数很多、或者映射表必须增量式 gossip 出去时，优先用环。相关的近亲：**Maglev hashing**，它构建一张查找表来实现 O(1) 命中和近乎完美的均衡，用于 L4 负载均衡。
