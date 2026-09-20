---
id: problems-key-value-store-quorum-availability-math
node: problems.foundations.key-value-store
type: qa
step: 3
tags: [grown]
---
## Q
In a leaderless key-value store with N=3 replicas and quorum reads/writes requiring 2 of 3 nodes, if each node independently has 99.9% steady-state availability, what is the resulting availability of a quorum operation, and roughly how much does that cut annual downtime?

## A
P(at least 2 of 3 available) = C(3,2)×0.999²×0.001 + 0.999³ = 0.002994 + 0.997003 ≈ 0.999997 (about 99.9997%). A single node at 99.9% availability accounts for about 525.6 minutes of downtime per year; the quorum's ~99.9997% availability cuts that to about 1.58 minutes per year — roughly a 333× reduction, purely from requiring only 2-of-3 independent nodes to agree instead of depending on one specific node.

## Q zh
在一个 N=3、读写都要求 3 个节点中 2 个响应的无主键值存储中，如果每个节点独立可用性是 99.9%，quorum 操作的可用性是多少？年停机时间大约缩短了多少？

## A zh
P(3 个中至少 2 个可用) = C(3,2)×0.999²×0.001 + 0.999³ = 0.002994 + 0.997003 ≈ 0.999997（约 99.9997%）。单节点 99.9% 可用性对应每年约 525.6 分钟停机；quorum 的约 99.9997% 可用性把它降到每年约 1.58 分钟——约缩短 333 倍，纯粹来自「只要求 3 个独立节点中的 2 个同意」而不是依赖某一个特定节点。
