---
id: hi-c-sd-elasticsearch-n11-how-it-works
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 11
---
## Q
**Elasticsearch · 它和 Lucene 是什么关系**｜摘要 · 必会

Elasticsearch 和 Apache Lucene 各负责什么？

## A
- **Lucene** 是高度优化的底层搜索库，搜索功能的"心脏"。
- **Elasticsearch** 是 Lucene 之上的高层编排框架，负责分布式系统的部分：集群协调、API、聚合、实时能力。
- **可以这样简化记忆：** Elasticsearch 是在一大堆 Lucene 索引之上叠了可用性和可扩展性。
