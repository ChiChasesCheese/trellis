---
id: aie-vector-index-which-store
node: t03.vector-index-ann-hnsw-ivf-product-quantization
type: qa
step: 2
tags: [考点]
---
## Q
**Vector index · 要不要专门上一个向量库**｜考点 · 追问

内部知识库只有 3 万个 chunk，团队想先买一个专门的向量数据库。你有什么看法？评估一个检索方案要问哪些问题？

## A
**规模决定做法：**
- 数据很小：直接做 k-NN 精确搜索也够，不需要 ANN 的近似和调参。
- 书里还提到：**任何能存向量的数据库都可以叫向量库**，传统数据库也在加入向量存储和搜索。所以先看现有的数据库扩展是否够用，再考虑新增一个系统。
- 数据大、查询多，才需要认真比较 ANN 索引。

**评估一个检索方案时问：**
1. 支持哪些检索机制？支持 hybrid search（关键词检索加向量检索一起用，后面细讲） 吗？
2. 如果是向量库，支持哪些 embedding 模型和搜索算法？
3. 数据量和查询流量上去之后伸缩性如何？
4. 索引你的数据要多久？一次能批量增删多少？
5. 不同检索算法的查询延迟？
6. 托管方案的计价方式：按向量量还是按查询量？

**别忘了：** embedding 检索要多出的延迟（生成查询向量、向量搜索）和一次回答的总延迟相比往往很小，因为大部分延迟来自生成输出；但成本要算清，向量库开销可能占到模型 API 的五分之一到一半。

**出处：** Huyen《AI Engineering》ch6 §Embedding-based retrieval、§Evaluating Retrieval Solutions、§Comparing retrieval algorithms
