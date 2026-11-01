---
id: hi-sd-ticketmaster-10-search
node: sd.problem-breakdowns.ticketmaster
type: qa
step: 10
---
## Q
**优化搜索：索引、全文索引到 Elasticsearch**｜系统设计 · 问题拆解

`LIKE '%Taylor%'` 为什么慢？搜索延迟有哪几级改进方案，各自的代价是什么？

## A
**为什么慢。** 前置通配符的 LIKE 无法用普通索引，只能全表扫描。

**1. 索引与查询优化。** 给活动名、日期、艺人名、场馆位置建索引；用 EXPLAIN、避免 `SELECT *`、加 LIMIT、用 UNION 代替 OR。但对子串匹配（搜 Taylor 而非 Taylor Swift）仍不理想，且索引占存储并拖慢写入。

**2. 数据库全文索引。** PostgreSQL 的 tsvector 加 GIN，MySQL 也有，比 LIKE 快得多，不基于 Lucene。代价：占更多空间，查询与维护更麻烦。

**3. Elasticsearch。** 倒排索引做全文搜索，还支持模糊搜索（容忍 Taylor 与 Tayler 的拼写差异），靠变更数据捕获（CDC）把 PostgreSQL 的增删改同步过去。代价：同步一致性难保证，集群增加基础设施和成本。

**取舍。** 面试里高级候选人应能说出用搜索引擎。
