---
id: ai-retrieve-then-rerank
node: ai.rag
type: qa
---
## Q
Why do production RAG systems use two stages — a fast retriever pulling top-100 and then a reranker cutting to top-5 — instead of one better retriever?

## A
It's the classic **candidate-generation + ranking** split from search/recsys, forced by a precompute trade-off:

- **Retriever (bi-encoder)**: embeds documents **ahead of time**; query time is one embed + ANN lookup over millions of vectors. Cheap and scalable, but the query and document never "see" each other — scoring is coarse. Optimize for **recall**.
- **Reranker (cross-encoder)**: scores each (query, document) **pair jointly** — far more accurate, but nothing can be precomputed, so it only affordably runs over ~100 candidates. Optimize for **precision**.

Result: recall from the cheap stage, precision from the expensive one, latency bounded by reranking a fixed small set. Feed the reranker from hybrid (BM25 + vector) retrieval for best coverage.

## Q zh
为什么生产 RAG 系统使用两个阶段 — 快速检索器拉前 100 个然后 reranker 切到前 5 个 — 而不是一个更好的检索器？

## A zh
这是来自搜索/recsys 的经典 **候选生成+排名** 分割，由预计算权衡强制：

- **检索器（bi-encoder）**：文档 **提前** 嵌入；查询时间是一个 embed + 对数百万向量的 ANN 查找。廉价且可扩展，但查询和文档永远不会"看到"彼此 — 评分粗糙。优化 **召回**。
- **Reranker（cross-encoder）**：**成对联合** 评分每个（查询、文档）— 更加准确，但没有什么可以预计算，所以它只能负担得起在 ~100 个候选上运行。优化 **精度**。

结果：廉价阶段的召回、昂贵阶段的精度、延迟由重新排名固定的小集合界定。从混合（BM25+向量）检索向 reranker 提供最佳覆盖。
