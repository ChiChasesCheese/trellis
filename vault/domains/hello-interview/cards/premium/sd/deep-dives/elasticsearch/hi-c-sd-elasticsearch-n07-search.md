---
id: hi-c-sd-elasticsearch-n07-search
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 7
---
## Q
**Elasticsearch · 查询：match、bool、nested**｜摘要 · 必会

三类基础查询怎么写？返回结果里有哪些内容？

## A
- **基于 JSON 的查询：** 语法类似 SQL，但是 JSON。`GET /books/_search`（带请求体的 GET；代理不接受就用 POST）。
- **全文匹配：** `{"match": {"title": "Great"}}`。
- **组合条件：** `bool` 里的 `must` 放多个子条件，如标题含 Great 并且 `range` 价格 `lte` 15。
- **嵌套字段：** 用 `nested` 查询，指定 `path` 为 `reviews`，里面再写 `bool`，才能保证"评论含 excellent 且评分不低于 4"是同一条评论满足。
- **响应：** `took`（耗时）、`_shards`、`hits.total`、每条命中的 `_score`（相关性分数）、`_source`（原始文档，除非另指定）。
