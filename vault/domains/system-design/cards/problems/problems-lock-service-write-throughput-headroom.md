---
id: problems-lock-service-write-throughput-headroom
node: problems.foundations.lock-service
type: cloze
step: 1
tags: [grown]
---
In a distributed lock/coordination service design serving a 5,000-client fleet, the actual demand for consensus-replicated writes (lock acquire/release, leader elections, config changes) works out to about {{c1::15 ops/second average, 75 at peak}} — two to three orders of magnitude below the roughly {{c2::18,000 writes/second}} a 5-node ensemble sustains in ZooKeeper's own published saturated-throughput benchmark, and {{c3::far below}} even the lowest tested ensemble size's write ceiling. This is why capacity planning for this class of service is dominated by fault-tolerance and latency reasoning, not by throughput headroom.

## zh
在一个为 5,000 个客户端提供服务的分布式锁/协调服务设计中，真正需要经过共识复制的写操作（锁获取/释放、leader 选举、配置变更）的实际需求约为 {{c1::平均每秒 15 次，峰值 75 次}}——比 ZooKeeper 论文自己发表的饱和吞吐实测里，5 节点集群约 {{c2::18,000 次/秒}} 的写上限低两到三个数量级，{{c3::甚至远低于}}实测中最小集群规模的写上限。这正是这类服务的容量规划由容错性和延迟推理主导、而不是由吞吐量余量主导的原因。
