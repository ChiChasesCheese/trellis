---
id: at-before-outside-retention-error
node: continuity.at-before-statement-syntax
type: qa
source: snowflake-docs
---
## Q
一张保留期（data retention period）为 1 天的表，执行 `SELECT * FROM t AT(OFFSET => -60*60*48)`（48 小时前）会返回什么？

## A
查询失败并报错。`AT | BEFORE` 指定的 TIMESTAMP、OFFSET 或 STATEMENT 如果落在表的数据保留期之外，那段历史数据已不在时间旅行（Time Travel）中，Snowflake 不会返回最接近的可用版本，而是直接报错。
