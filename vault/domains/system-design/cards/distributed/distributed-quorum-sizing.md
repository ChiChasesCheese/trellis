---
id: distributed-quorum-sizing
node: distributed.consensus
type: cloze
---
Consensus tolerating f crashed nodes requires {{c1::2f + 1}} nodes (majority quorums must intersect) — so 3 nodes tolerate 1 failure, 5 tolerate 2. A 4-node cluster tolerates {{c2::still only 1 failure (majority is 3), which is why even cluster sizes are pointless}}. Every committed write costs {{c3::a round-trip to the slowest node of the fastest majority}}, which is the latency argument against stretching a consensus group across distant regions.

## zh
要容忍 f 个节点崩溃的共识需要 {{c1::2f + 1}} 个节点（多数派 quorum 之间必须相交）——所以 3 个节点容忍 1 个故障，5 个容忍 2 个。4 个节点的集群{{c2::仍然只容忍 1 个故障（多数派是 3），这就是为什么偶数规模的集群没有意义}}。每一次提交的写都要付出{{c3::一个到"最快多数派中最慢那个节点"的往返}}，这正是反对把一个共识组拉长跨越遥远地域的延迟论据。
