---
id: distributed-quorum-math
node: distributed.replication.leaderless
type: cloze
---
Leaderless replication with N replicas: reads see the latest acknowledged write when {{c1::W + R > N}} (write and read sets must intersect). With N=3, W=2, R=2 you tolerate {{c2::one}} replica down for both reads and writes. Setting W=1, R=1 maximizes availability/latency but reads can miss recent writes. Caveat: {{c3::sloppy quorums (writes landing on non-home nodes during faults)}} break the intersection guarantee even when W + R > N — Dynamo-style stores need hinted handoff plus read repair/anti-entropy to converge.

## zh
N 个副本的无主复制：当 {{c1::W + R > N}} 时，读一定能看到最近一次被确认的写（写集合与读集合必须相交）。N=3、W=2、R=2 时，读和写都能容忍{{c2::一个}}副本宕机。设成 W=1、R=1 可用性和延迟最好，但读可能漏掉刚写入的数据。注意：{{c3::sloppy quorum（故障期间写落到非归属节点上）}}会破坏这个相交保证，即使 W + R > N 也一样——Dynamo 式的存储要靠 hinted handoff 加上 read repair/anti-entropy 才能收敛。
