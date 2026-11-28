---
id: hi-c-sd-elasticsearch-n04-basic-use-create
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 4
---
## Q
**Elasticsearch · 建索引和设置映射**｜摘要 · 必会

怎么创建索引？什么时候要提前设映射，嵌套字段怎么声明？

## A
- **建索引：** 一个 `PUT /books` 就会创建索引，带动态映射、默认 1 个分片、1 个副本；`number_of_shards` 和 `number_of_replicas` 可以在设置里指定。
- **动态映射不合适时先设映射：** 比如数据里多数字段根本不用搜索。`PUT /books/_mapping` 预先声明要可搜索的字段和类型（`title` 用 `text`，`author`、`categories` 用 `keyword`，`price` 用 `float`，`publish_date` 用 `date`）。添加文档时，Elasticsearch 会提取这些字段建索引。
- **嵌套字段：** `reviews` 声明为 `nested`，每条评论是带自己字段（`user`、`rating`、`comment`）的嵌套文档，而不是拍平；这样"同一条评论里评分高且评论里有某词"能被正确匹配。
- **映射可随时间演进：** 但已有字段的类型不能原地更改。
