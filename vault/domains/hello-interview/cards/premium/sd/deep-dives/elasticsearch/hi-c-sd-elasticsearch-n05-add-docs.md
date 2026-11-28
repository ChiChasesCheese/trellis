---
id: hi-c-sd-elasticsearch-n05-add-docs
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 5
---
## Q
**Elasticsearch · 添加文档，响应里的 `_version` 是什么**｜摘要 · 必会

怎么把文档加进索引？响应里哪个字段与并发更新有关？

## A
- **添加：** 对 `/books/_doc` 发 POST，请求体是文档 JSON；再发一次就再加一个。
- **响应：** 包含文档 ID（`_id`）、`result: created`、分片情况（`_shards` 里总数、成功、失败）、`_seq_no`、`_primary_term`。
- **`_version`：** 文档的版本号，它随每次修改递增，也可作外部版本号；做乐观并发控制时，应使用 `_seq_no` 与 `_primary_term`。
