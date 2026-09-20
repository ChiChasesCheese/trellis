---
id: problems-key-value-store-gossip-convergence-log-n
node: problems.foundations.key-value-store
type: qa
step: 7
tags: [grown]
---
## Q
In a key-value store that manages cluster membership with a gossip protocol instead of a centralized coordination service, why does membership convergence time scale well as the cluster grows from about 167 nodes to about 1,700 nodes?

## A
Gossip convergence rounds scale roughly as log2(N): log2(167) ≈ 7.4, so about 8 rounds; log2(1,700) ≈ 10.7, so about 11 rounds — a 10x increase in node count adds only 3 more rounds. This logarithmic (not linear) scaling is why gossip-based membership stays viable at hundreds to thousands of nodes without a centralized coordination service, which would instead make its own availability and write throughput the ceiling on how fast membership changes propagate.

## Q zh
在一个用 gossip 协议而不是中心化协调服务来管理集群成员的键值存储中，为什么从约 167 台节点扩容到约 1,700 台节点时，成员收敛时间依然扩展得很好？

## A zh
gossip 的收敛轮数大致按 log2(N) 增长：log2(167) ≈ 7.4，约 8 轮；log2(1,700) ≈ 10.7，约 11 轮——节点数增长 10 倍，只多了 3 轮。这种对数（而非线性）的扩展性，正是 gossip 式成员管理能在成百上千节点规模下不依赖中心化协调服务的原因；换成中心化协调服务，它自身的可用性和写吞吐会反过来成为成员变更传播速度的天花板。
