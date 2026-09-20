---
id: problems-social-graph-search-bidirectional-bfs-exponent-halving
node: problems.social.social-graph-search
type: qa
step: 5
tags: [grown]
---
## Q
For finding the shortest path (degree of separation) between two users in a social graph with an average of 300 connections per user, why does bidirectional BFS explore roughly 2×300^2 = 180,000 nodes to find a distance-4 path, while a single-direction BFS from one user would need to explore on the order of 300^4 ≈ 8.1 billion — a difference of about 45,000x?

## A
A single-direction search's explored-node count grows as (branching factor)^(full distance), so at distance 4 it grows to 300^4, a number close to the entire user base's size. A bidirectional search expands from both endpoints simultaneously and only needs each side to reach the midpoint, at distance/2 hops, so its cost is roughly 2×(branching factor)^(distance/2) — halving the exponent rather than the base, which produces an exponential reduction in work, not just a constant-factor speedup.

## Q zh
在一个人均 300 个连接的社交图里查找两个用户之间的最短路径（分隔度）时，为什么双向 BFS 找到一条距离为 4 的路径大约只需要探索 2×300^2 = 180,000 个节点，而从一端出发的单向 BFS 大约需要探索 300^4 ≈ 81 亿个节点——相差约 4.5 万倍？

## A zh
单向搜索探索过的节点数随（分支因子）的（完整距离次方）增长，所以在距离为 4 时会长到 300^4，这个数字已经接近全站用户总数。双向搜索从两端同时扩展，每一端只需要走到中点，即 距离/2 跳，所以代价大约是 2×（分支因子）^（距离/2）——减半的是指数而不是底数，带来的是指数级的工作量下降，不只是一个常数倍的加速。
