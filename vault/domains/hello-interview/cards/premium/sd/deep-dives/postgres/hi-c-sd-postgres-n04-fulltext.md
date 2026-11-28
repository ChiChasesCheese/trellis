---
id: hi-c-sd-postgres-n04-fulltext
node: sd.deep-dives.postgres.notes
type: qa
step: 4
---
## Q
**PostgreSQL · 全文搜索：GIN 索引**｜摘要 · 必会

PostgreSQL 内置的全文搜索怎么工作？什么时候仍然该上 Elasticsearch？

## A
- **tsvector 列加 GIN 索引：** GIN（Generalized Inverted Index）：倒排索引，像书末的索引，记录每个词出现在哪些文档里，所以按词查文档很快。做法是加一列 `tsvector`，在该列建 GIN 索引，用 `@@ to_tsquery(...)` 查询。
- **自带能力：** 词干还原（finding / find / finds 互相匹配）、相关性排序、多语言、AND/OR/NOT 组合查询。
- **多数应用够用：** 可以省掉单独的 Elasticsearch 集群，架构更简单、运维更少。
- **该上 Elasticsearch 的信号：** 更精细的相关度评分、分面搜索（faceted search）、模糊匹配和边输入边搜索、跨超大数据集的分布式搜索、复杂的分析聚合。
- **顺序：** 先用内置搜索，出现它满足不了的具体需求再引入。
