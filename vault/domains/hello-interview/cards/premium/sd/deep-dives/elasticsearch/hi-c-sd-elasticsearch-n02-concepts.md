---
id: hi-c-sd-elasticsearch-n02-concepts
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 2
---
## Q
**Elasticsearch · 文档、索引、映射、字段**｜摘要 · 必会

Elasticsearch 的四个基本概念各是什么？`keyword` 和 `text` 的区别是什么？

## A
- **文档（document）：** 被搜索的基本单位，就是一个 JSON 对象，不必是网页或博客。
- **索引（index）：** 文档的集合，每个文档有唯一 ID 和一组字段（键值对），可以类比数据库的表；搜索就在索引上进行。注意"索引"这个词被重载：它也泛指让搜索变快的辅助数据结构，要说清是哪一种。
- **映射（mapping）：** 索引的模式，定义有哪些字段、各自的类型、怎么处理和索引。你可以往文档里放任何数据，但哪些字段可搜索、是什么类型，由映射决定。类型可以很复杂：嵌套对象和数组、`geo_point` / `geo_shape` 地理类型、自定义分析器、用于语义搜索的向量嵌入。
- **`keyword` 与 `text`：** `keyword` 把整个值当作一个整体，适合 ID、枚举，类似哈希表的精确查找；`text` 会被分词，建立倒排索引，适合"标题包含某个词"这类查询。
