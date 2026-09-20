---
id: problems-search-engine-multipass-candidate-funnel
node: problems.search.search-engine
type: qa
step: 5
tags: [grown]
---
## Q
In a search system over a 59.3-billion-document corpus, a two-term AND query where each term covers 2% of documents produces about 23.7 million intersection candidates (59.3B x 0.02^2). Running an expensive reranking model on every one of those candidates at 1,157 average queries/second would require about 27.4 billion reranker calls/second. What architecture avoids this, and roughly how much does it cut reranker load by?

## A
A narrowing funnel: inverted-index intersection produces the full raw candidate set (millions), a cheap term-frequency-based score (e.g. BM25-style) trims that down to about 2,000 candidates without running any model, and the expensive reranking model only runs on the roughly 100 candidates that survive after merging each shard's local top-K. At 1,157 average QPS, that's about 115,700 reranker calls/second instead of 27.4 billion — a reduction of roughly 237,250x, because the expensive computation only ever touches the small candidate set at the end of the funnel.

## Q zh
在一个 593 亿文档规模的搜索系统中，一个两词 AND 查询（每个词覆盖 2% 的文档）产生约 2,372.5 万个求交候选（593 亿 × 0.02^2）。如果在平均 1,157 QPS 的查询量下对每一个候选都跑一次昂贵的重排模型，需要约每秒 274 亿次重排调用。什么样的架构能避免这一点，大约能把重排负载降低多少？

## A zh
一个逐层收窄的漏斗：倒排表求交先产出全部原始候选（数百万到千万级），一个廉价的基于词频的打分（类似 BM25）不跑任何模型就把候选收窄到约 2,000 条，昂贵的重排模型只对合并各分片本地 top-K 后剩下的约 100 条候选运行。按 1,157 平均 QPS 折算，重排调用量约为每秒 115,700 次，而不是 274 亿次——降低约 237,250 倍，因为昂贵的计算自始至终只触碰漏斗末端的小候选集。
