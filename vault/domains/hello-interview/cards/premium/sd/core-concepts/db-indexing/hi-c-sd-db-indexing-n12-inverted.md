---
id: hi-c-sd-db-indexing-n12-inverted
node: sd.core-concepts.db-indexing.notes
type: qa
step: 12
---
## Q
**数据库索引 · 倒排索引与全文搜索**｜摘要 · 必会
`LIKE '%database%'` 为什么用不了 B 树？倒排索引怎么解决，有什么代价？

## A
- **B 树的限制：** 它只能帮前缀匹配（`'database%'`），或对反转后的内容建索引做后缀匹配；模式可能出现在文本任意位置时，数据库只能把每篇文章读进内存逐字符比对，文本越长越慢。
- **倒排索引（inverted index）：** 把关系反过来，不是"文档里有哪些词"，而是"词出现在哪些文档"，像教材末尾的索引页。例如 `b-trees -> [doc1, doc3]`，`fast -> [doc1, doc2]`。
- **生产系统的分析流水线：** 分词、转小写、去停用词（the、and）、词干化，因此搜"Databases"能匹配 database、DATABASE。Elasticsearch、Lucene 还在此基础上提供词频、相关度打分、模糊匹配（databas）、短语查询。
- **常见用途：** 代码仓库搜索、聊天记录搜索、文档搜索。
- **代价：** 存储开销大；文档变化时要更新它含有的每个词的条目。
