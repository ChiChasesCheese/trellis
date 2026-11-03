---
id: hi-sd-key-technologies-3-search-db
node: sd.in-a-hurry.key-technologies.exam
type: qa
step: 3
---
## Q
**搜索型数据库与倒排索引**｜系统设计 · 速览

全文搜索为什么不能靠 LIKE '%词%'？搜索型数据库靠什么做到快，面试里要懂哪些概念？

## A
**问题。** `LIKE '%词%'` 无法利用索引，要全表扫描，把每行都取出来判断，数据量大时无法扩展。

**机制。** 搜索型数据库建立倒排索引（inverted index）：从词到包含它的文档列表的映射，查询时直接按词查找，不扫表。

**要懂的概念。**
- 分词（tokenization）：把文本切成词
- 词干提取（stemming）：把 running、runs 归约为 run，匹配同词的不同形态
- 模糊搜索（fuzzy search）：用编辑距离容忍拼写错误，多数产品作为配置项提供
- 扩展：和普通数据库一样，加节点、分片

**选型。** 首选 Elasticsearch（基于 Lucene）。也可以用已有数据库的能力，如 Postgres 的 GIN 索引支持全文搜索，能缩小系统占用面，但要知道它的存在。

**使用时机。** Ticketmaster 搜活动、Twitter 搜推文这类需求。资深候选人若讲不出倒排索引和其扩展方式，会被记为黄牌。
