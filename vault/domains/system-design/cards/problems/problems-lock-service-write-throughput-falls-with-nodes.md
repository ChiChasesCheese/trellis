---
id: problems-lock-service-write-throughput-falls-with-nodes
node: problems.foundations.lock-service
type: qa
step: 7
tags: [grown]
---
## Q
In a distributed lock/coordination service design, why is adding more voting nodes to a single consensus ensemble never a way to increase its write throughput — and what does ZooKeeper's own published saturated-throughput data (3, 5, 7, 9, 13-node ensembles at 100% writes: roughly 21k, 18k, 14k, 12k, 8k ops/sec respectively) show about the actual effect?

## A
Every write in a consensus-replicated service must be durably copied to and acknowledged by a majority of voting nodes before it commits, so adding voters adds more replication targets and a slower quorum round-trip to every single write — write throughput falls as ensemble size grows, exactly as ZooKeeper's own data shows (it drops from about 21k ops/sec at 3 nodes to about 8k ops/sec at 13 nodes). Reads behave oppositely and rise with more nodes, since each additional replica is another node that can answer a local read. The only thing more voters buys is fault tolerance (via 2f+1), never throughput — so scaling this class of service means running more independent ensembles, not growing one ensemble larger.

## Q zh
在一个分布式锁/协调服务设计中，为什么给单个共识集群增加更多投票节点永远不能提高它的写吞吐量？ZooKeeper 自己发表的饱和吞吐实测数据（3、5、7、9、13 节点集群在 100% 写负载下分别约为 21k、18k、14k、12k、8k 次/秒）说明了实际效果是什么？

## A zh
在一个共识复制的服务里，每一次写都必须被持久复制到多数投票节点并获得确认才能提交，所以增加投票节点等于给每一次写都增加了更多的复制目标和更慢的 quorum 往返——写吞吐量会随集群规模增大而下降，这正是 ZooKeeper 自己的数据所展示的（从 3 节点约 21k 次/秒降到 13 节点约 8k 次/秒）。读的表现恰好相反，会随节点数增加而上升，因为每多一个副本就多一个能在本地回答读请求的节点。多投票节点唯一换来的是容错能力（通过 2f+1），从来不是吞吐量——所以要扩展这类服务的规模，做法是部署更多独立的集群，而不是让一个集群越长越大。
