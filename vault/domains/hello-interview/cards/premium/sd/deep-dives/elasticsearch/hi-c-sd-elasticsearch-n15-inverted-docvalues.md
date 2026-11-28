---
id: hi-c-sd-elasticsearch-n15-inverted-docvalues
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 15
---
## Q
**Elasticsearch · 倒排索引与 doc values**｜摘要 · 必会

倒排索引为什么让关键词搜索快？doc values 解决什么问题？

## A
- **让检索快的两条路：** 按检索方式组织数据（无序表 O(n)、有序列表 O(log n)、哈希表 O(1)）；或者复制一份数据并按那种方式组织。
- **倒排索引（inverted index）：** 把内容（词）映射到它所在的文档。列出每个出现过的词，及其出现在哪些文档。10 亿册图书里找标题含 "lazy" 的，不必扫描，直接查倒排索引得到文档 #12、#53 之类。这用复制数据加巧妙组织，把 O(n) 扫描变成近似 O(1) 的查找。
- **doc values：** 倒排索引给出词到文档，但要按价格排序时只需要匹配结果的价格。行存储的关系库为取一列也要读整行。doc values 是列式的：同一字段在段内所有文档的值连续存放，像 Spark、Redshift 那样读一列就是读一块连续内存。倒排索引找出文档，doc values 提供排序和聚合所需的数据。
