---
id: hi-sd-elasticsearch-1-concepts-mapping
node: qb.sd.hotel-booking-system.pre-sd-deep-dives-elasticsearch
type: qa
step: 1
---
## Q
**文档、索引、映射与 text/keyword**｜系统设计 · 深入技术

Elasticsearch 的文档（document）、索引（index）、映射（mapping）各是什么？为什么映射里 keyword 和 text 要区分，映射写太多字段有什么代价？

## A
**概念。** 文档是被搜索的单元，可看作一个 JSON 对象；索引是文档的集合，类似数据库的表；映射是索引的模式，定义有哪些字段、什么类型、怎样处理与索引。注意这里的「索引」与泛指加速查找的辅助结构不是一个词义。

**keyword 与 text。** keyword 把整个值当一个整体，适合精确匹配与排序，像哈希表查 id；text 会分词，适合「标题里是否包含某词」的全文搜索，靠倒排索引。

**代价。** 映射里放了实际不搜索的字段，会白白增加每个索引的内存开销。10 个字段只搜 2 个，就别全映射。查询性能的大部分调优都落在映射和集群参数上。
