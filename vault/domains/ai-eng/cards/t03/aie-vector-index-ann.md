---
id: aie-vector-index-ann
node: t03.vector-index-ann-hnsw-ivf-product-quantization
type: qa
step: 1
tags: [摘要]
---
## Q
**Vector index · 为什么需要 ANN，几种方法怎么分**｜摘要 · 必会

向量库里有 5,000 万个向量，每次查询都和全部向量算一遍相似度太慢。常见的 ANN 方法各是什么思路？评测它们看哪几项？

## A
**精确方法（k-NN）：** 查询向量和库里**每个**向量算相似度（如 cosine similarity），排序，取最高的 k 个。结果精确，但计算量大、慢，**只适合小数据集**。

**ANN（approximate nearest neighbor）：** 不保证找到绝对最近的，但快得多。思路是把向量组织成桶、树或图，让相似的向量彼此靠近；也可以量化（降低精度）或稀疏化来省计算。

| 方法 | 思路 |
|---|---|
| **LSH** | 把相似向量哈希进同一个桶，用一点精度换速度 |
| **HNSW** | 建多层图，节点是向量、边连相似的向量，沿边遍历找近邻 |
| **IVF** | K-means 把相似向量分到同一簇；查询时先找最近的簇中心，只搜这些簇。每簇平均约 100–10,000 个向量 |
| **Product quantization（PQ）** | 把每个向量拆成多段子向量，用更低维的简化表示算距离，更快更省 |
| **Annoy** | 建多棵随机二叉树，沿树收集候选 |

IVF 常与 PQ 合用，是 FAISS 的核心。

**怎么比（ANN-Benchmarks 的四项）：**

| 指标 | 含义 |
|---|---|
| Recall | 找到了多少真正的最近邻 |
| QPS | 每秒处理多少查询，高流量应用看它 |
| Build time | 建索引的时间；数据常更新就很重要 |
| Index size | 索引大小，决定能不能扩展 |

**收益与代价：** 越精细的索引（如 HNSW）查询准且快，但**建索引慢、占内存多**；简单的索引（如 LSH）建得快、省内存，查询慢且不够准。

**出处：** Huyen《AI Engineering》ch6 §Embedding-based retrieval（k-NN、ANN 各算法）、§Comparing retrieval algorithms（ANN-Benchmarks）
