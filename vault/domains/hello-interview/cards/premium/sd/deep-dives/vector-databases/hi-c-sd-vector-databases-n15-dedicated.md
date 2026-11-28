---
id: hi-c-sd-vector-databases-n15-dedicated
node: sd.deep-dives.vector-databases.notes
type: qa
step: 13
---
## Q
**向量数据库 · 什么时候需要专用向量数据库**｜摘要 · 必会

哪种规模和需求才该用专用向量数据库？几个主要产品各自的定位是什么？

## A
- **经验法则：** 超过约 1 亿个向量，或问题本身的核心就是检索/推荐，才考虑专用库。
- **Pinecone：** 全托管、无服务器，不用运维，调 API 即可，最容易运行；代价是成本和控制力。
- **Weaviate：** 开源，混合搜索支持好，GraphQL API；介于自己搭和全托管之间。
- **Milvus：** 开源，为大规模而建，能处理数十亿向量；代价是运维复杂，要跑有多种节点类型的分布式系统。
- **Qdrant：** 开源，用 Rust 写成，过滤支持特别好；复杂过滤查询是核心时值得考虑。
- **Chroma：** 轻量，适合原型，在 LLM/RAG 圈子里因为易上手而流行。
