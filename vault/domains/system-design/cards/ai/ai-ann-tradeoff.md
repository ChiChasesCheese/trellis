---
id: ai-ann-tradeoff
node: ai.vector-search
type: cloze
---
Exact nearest-neighbor search over embeddings is a linear scan — O(N·d) per query — so vector databases use **ANN** indexes, which trade {{c1::perfect recall (they may miss some true neighbors)}} for {{c2::sublinear query time}}. Recall vs latency is tunable at query time (e.g. HNSW `efSearch`, IVF `nprobe`), so you benchmark recall@k on your own data instead of trusting defaults.

## zh
基于 embedding 的精确最近邻搜索是线性扫描 — O(N·d) 每次查询 — 所以向量数据库使用 **ANN** 索引，它用 {{c1::perfect recall (they may miss some true neighbors)}} 换取 {{c2::sublinear query time}}。Recall vs latency 可以在查询时调整（例如 HNSW `efSearch`、IVF `nprobe`），所以你应该在自己的数据上基准测试 recall@k，而不是相信默认值。
