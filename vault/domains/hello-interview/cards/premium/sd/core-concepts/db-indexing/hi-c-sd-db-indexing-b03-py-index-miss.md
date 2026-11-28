---
id: hi-c-sd-db-indexing-b03-py-index-miss
node: sd.core-concepts.db-indexing.beyond
type: qa
step: 3
---
## Q
**数据库索引 · 为什么加了索引还是不走**｜拓展 · 加分
明明在 `email` 上有索引，哪些写法会让数据库不用它？怎么确认？

## A
- **在列上套函数：** `WHERE lower(email) = 'a@b.com'` 无法用普通 `email` 索引；解决：建函数（表达式）索引 `ON users (lower(email))`，或写入时统一小写。
- **前导通配符：** `LIKE '%abc'` 用不了 B 树；前缀 `LIKE 'abc%'` 可以（在合适的排序规则下）。
- **类型隐式转换：** 列是字符串而参数是数字（或相反），可能导致转换作用在列上，从而用不上索引。
- **选择性太低：** 条件命中一半以上的行时，优化器宁可顺序扫描，因为随机读很多页比顺序读还慢。
- **统计信息过期：** 优化器估算错误，选错了计划；需要更新统计信息。
- **确认方法：** 看 `EXPLAIN`（PostgreSQL 用 `EXPLAIN ANALYZE`）的查询计划，看是 Index Scan / Index Only Scan，还是 Seq Scan，以及估计行数与实际行数的差距。
- **面试价值：** 说"我会先看查询计划再决定加索引"，显得有生产经验。
