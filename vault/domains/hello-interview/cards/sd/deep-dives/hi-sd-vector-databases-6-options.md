---
id: hi-sd-vector-databases-6-options
node: sd.deep-dives.vector-databases
type: qa
step: 6
---
## Q
**选型：先用扩展，超大规模再专用**｜系统设计 · 深入专题

面试里引入向量检索，应该直接选专用向量数据库吗？各选项的取舍是什么？

## A
**要点。** 先从简单的开始：已有的数据库加向量扩展，几百万向量完全够用，还不用多运维一套系统。

| 选项 | 适用 |
|---|---|
| pgvector | 已经用 PostgreSQL，支持 HNSW 和 IVF，还有事务和与关系数据联表的能力 |
| Elasticsearch kNN | 已有 ES，关键词加向量混合搜索开箱即用 |
| Redis 向量搜索 | 要实时低延迟，索引选项较简单 |
| S3 Vectors | 数据已在 S3，不想再加系统 |
| Pinecone | 全托管无服务器，最省运维，贵且控制少 |
| Weaviate / Milvus / Qdrant / Chroma | 开源；Milvus 可到十亿级但运维复杂，Qdrant 过滤强，Chroma 适合原型 |

**数字。** 经验线：超过约 1 亿向量，再考虑专用库。

**易错。** 低估再运维一套分布式系统的成本；或者反过来，在小规模上直接上专用库。
