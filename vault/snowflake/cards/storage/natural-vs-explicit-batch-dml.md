---
id: natural-vs-explicit-batch-dml
node: storage.natural-vs-explicit-clustering
type: qa
source: snowflake-docs
---
## Q
一张表查询很多、写入也很频繁，又确实需要显式聚簇，怎样降低维护聚簇的成本？

## A
把 DML 语句合并成大批量、低频率地执行。表变动越频繁，保持聚簇越贵：每次零散写入都可能让聚簇状态漂移并触发微分区（micro-partition）重写。聚簇在“查询次数与 DML 次数之比很高”的表上最划算，把写入攒批就是在人为提高这个比值。
