---
id: hi-c-sd-cassandra-n01-what-is
node: sd.deep-dives.cassandra.notes
type: qa
step: 1
---
## Q
**Cassandra · 它是什么、适合什么**｜摘要 · 必会

Cassandra 是什么类型的数据库？它的血统和核心特点是什么？

## A
- **定位：** 开源的分布式 NoSQL 数据库，采用分区的宽列（wide-column）存储，语义是最终一致（eventual consistency）。
- **血统：** 把 Dynamo 的分布式思路（一致性哈希、无主复制、可调一致性）和 Bigtable 的存储模型（LSM 树、宽列）结合起来。
- **起源：** Facebook 为收件箱搜索而做，要应付海量数据和写入；之后被 Discord、Netflix、Apple 等采用。
- **扩展方式：** 加廉价机器做水平扩展，集群里没有特殊主节点。
- **一句话定位：** 为高写入吞吐、高可用、可无限水平扩展而生，代价是查询灵活性和强一致。
