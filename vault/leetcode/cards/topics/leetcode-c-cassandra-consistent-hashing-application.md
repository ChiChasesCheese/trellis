---
id: leetcode-c-cassandra-consistent-hashing-application
node: topics.uncategorised
type: qa
anki: 1787359912793
tags: [algorithm::consistent-hashing, algorithm::hash-ring, algorithm::quorum-intersection, algorithm::virtual-nodes, application, case, case::cassandra-consistent-hashing, category::distributed-streaming, leetcode, system::apache-cassandra]
---
## Q
Cassandra 的 consistent hashing、vnodes 和 quorum 分别解决什么问题？

## A
consistent hashing 把 partition key 映射到 token ring，使节点变化只迁移少量相邻 ranges；vnodes 让一个物理节点拥有多个小 range，改善均衡和迁移粒度；quorum 决定一次读写等待多少 replicas，并通过读写集合相交获得可见性保证。

**Evidence**

Cassandra 官方 Dynamo 文档分别描述 token ring、vnodes 的收益与代价，以及 R + W > RF 的 quorum intersection。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FCassandra%20%E4%B8%80%E8%87%B4%E6%80%A7%E5%93%88%E5%B8%8C%E4%B8%8E%20Token%20Ring)
