---
id: hi-c-sd-yelp-b01-pg-search-types
node: sd.problem-breakdowns.yelp.beyond
type: qa
step: 1
---
## Q
**Yelp · 拓展：Postgres 里到底用什么索引做名称和位置**｜拓展 · 追问

用 Postgres 做名称加位置搜索，到底该建什么索引？`pg_trgm` 是全文搜索吗？PostGIS 的空间索引是四叉树吗？

## A
- **名称的全文搜索：** Postgres 内置的全文搜索用 `tsvector`（分词后的文档）和 `tsquery`，配合 GIN 倒排索引，按词查询。它不是 `pg_trgm`。
- **`pg_trgm` 是什么：** 把字符串切成三个字符一组（trigram），做相似度匹配，并能让 `LIKE '%coffee%'`、`ILIKE` 和容错拼写使用 GIN 或 GiST 索引。适合模糊匹配和子串，不是按词和词干的全文检索。
- **PostGIS 的空间索引：** 默认用 GiST，是 R 树的一种实现，不是四叉树；也有 SP-GiST 可以实现四叉树类的结构。查询用 `ST_DWithin`（按距离）时会利用这个索引，用 `geography` 类型时距离单位是米。
- **所以答案：** 名称用 `tsvector` 加 GIN（或 trigram 做模糊），位置用 GiST 空间索引；先用空间索引缩小候选，再按名称和类别过滤。面试里说"空间索引（R 树或四叉树）"都对，但别把扩展名称说错。
- **模式。** 一个查询多种索引：不同类型的过滤交给最合适的索引，由查询规划器组合。
