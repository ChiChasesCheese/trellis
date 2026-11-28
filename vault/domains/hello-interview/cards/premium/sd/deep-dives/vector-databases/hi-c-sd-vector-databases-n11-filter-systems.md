---
id: hi-c-sd-vector-databases-n11-filter-systems
node: sd.deep-dives.vector-databases.notes
type: qa
step: 9
---
## Q
**向量数据库 · 三类系统怎么处理过滤，以及混合搜索**｜摘要 · 必会

pgvector、Elasticsearch、Pinecone 在过滤上有何不同？混合搜索是什么？

## A
- **pgvector：** 依赖 Postgres 查询规划器，写普通 SQL（`WHERE` 加按向量距离 `ORDER BY`），规划器决定走向量索引、过滤列的 B 树，还是组合。过滤很严格时常直接跳过向量索引，对筛后行暴力计算，反而更快。局限：用向量索引时过滤发生在索引扫描之后（后过滤），过滤较严时可能返回不足 K 条；0.8.0 起可开迭代索引扫描（iterative index scan），继续往下扫索引直到凑够结果或到扫描上限，但本质仍是后过滤，选择性在中间地带时计划可能不佳。
- **Elasticsearch：** kNN 支持 `filter` 参数，在遍历索引时应用而不是事后；条件越严格要遍历的图越多、越慢，但只要存在就保证返回 K 个；原生支持混合搜索（BM25 关键词加向量相似度）。
- **Pinecone 这类专用库：** 元数据过滤是一等功能，每个向量可带任意元数据（最多 40 KB），过滤在 ANN 搜索过程中进行，内部为元数据字段建位图索引（roaring bitmap），查询时按过滤的选择性选先过滤或扫描中过滤，不做事后过滤。
- **混合搜索（hybrid search）：** 如"红色跑鞋"，关键词匹配"红色""跑鞋"，同时用向量找语义相关商品。并行做两种搜索再合并，通常比单独一种更好。
