---
id: hi-sd-fb-post-search-3-inverted-index
node: sd.problem-breakdowns.fb-post-search
type: qa
step: 3
---
## Q
**关键词搜索：倒排索引**｜系统设计 · 题目拆解

帖子搜索要在万亿帖子中按关键词查找。请说明为什么未建索引的数据库加分片走不通，倒排索引（inverted index）怎样工作，以及用 Redis 实现时的代价。

## A
**不建索引（死路）。** 用 `LIKE '%关键词%'` 要在查询时检查每一帖。分片或复制只把 N 帖分摊成 N/M，依然慢得不可接受。

**倒排索引。** 建一张“关键词到包含它的帖子 ID 列表”的字典。写入时，摄取服务（Ingestion Service）先分词（tokenization），把帖子 ID 追加到每个关键词对应的列表；查询直接取该关键词的列表。放在 Redis 内存里，查询极快，持久性问题可以换成 MemoryDB 之类的持久化方案，或在深挖里处理。

**代价。** 常见关键词的 ID 列表会非常大；一帖有 10 到 1000 个关键词，每帖要写很多个键。这两点是后面写入扩展和存储优化的主题。
