---
id: distributed-vnode-count
node: distributed.partitioning.schemes
type: cloze
---
Choosing the number of virtual nodes (tokens) per physical node is a variance-vs-overhead trade: with V random tokens per node, load imbalance shrinks roughly as {{c1::1/sqrt(V)}}, which is why naive random placement needs V in the hundreds (Cassandra's historic default was {{c2::256 tokens per node}}) to keep ownership within a few percent of even. The cost of a large V is {{c3::more ranges to track in the ring/metadata, and repair and streaming fragmenting into many small ranges — Merkle-tree repair and bootstrap get slower and more IO-bound}}. Modern deployments therefore drop V drastically (Cassandra 4+ recommends {{c4::16 tokens with the allocation algorithm, which places tokens deliberately to balance load instead of relying on randomness}}). Rendezvous hashing and bounded-load variants sidestep the tuning entirely.

## zh
选择每个物理节点的虚拟节点（令牌）数量是方差vs开销权衡：每个节点有 V 个随机令牌，负载不平衡大约收缩为 {{c1::1/sqrt(V)}}，这就是为什么天真随机放置需要 V 在数百个（Cassandra 历史默认是 {{c2::每节点 256 个令牌}}）以保持所有权在几个百分比内。大 V 的成本是 {{c3::环/元数据中更多范围要跟踪，修复和流变成许多小范围 — Merkle 树修复和引导变得更慢和更 I/O 绑定}}。现代部署因此大幅降低 V（Cassandra 4+ 推荐 {{c4::使用分配算法的 16 个令牌，故意放置令牌以平衡负载而不是依赖随机性}}）。会合哈希和有界负载变体完全避免了调谐。
