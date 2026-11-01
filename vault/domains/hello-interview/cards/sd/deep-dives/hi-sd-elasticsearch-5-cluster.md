---
id: hi-sd-elasticsearch-5-cluster
node: qb.sd.hotel-booking-system.pre-sd-deep-dives-elasticsearch
type: qa
step: 5
---
## Q
**集群架构：节点类型、分片与两阶段查询**｜系统设计 · 深入技术

Elasticsearch 集群有哪些节点类型？索引、分片、副本、Lucene 索引是什么关系？一次搜索怎么执行？

## A
**节点类型。** master 管集群级操作（增删节点、建删索引），启动时由种子节点选主；data 存数据；coordinating 接客户端查询并分发合并；ingest 做摄入前转换；ML 节点做机器学习。一台实例可兼任多种；data 节点还分 hot / warm / cold / frozen。

**嵌套关系。** 索引由分片及其副本组成，一个分片对应一个 Lucene 索引，Lucene 索引由段组成。副本既提高可用性，也提高吞吐：单分片 X TPS，Y 个副本约 X*Y。

**执行。** 先 query 阶段在各分片并行用索引结构找出文档 id，协调节点合并排序，再 fetch 阶段按需取 `_source`。最好的查询根本不用碰源文档。
