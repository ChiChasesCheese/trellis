---
id: result-cache-result-scan-postprocess
node: cache.result-cache
type: qa
source: snowflake-docs
---
## Q
`SHOW TABLES`、`DESCRIBE <object>` 这类命令返回的结果不能像普通 SELECT 那样被直接嵌套进另一条复杂 SQL 语句中，如果想对它们的输出结果做进一步过滤或联接，应该怎么做？

## A
可以使用 `RESULT_SCAN` 表函数，把上一条已执行语句的持久化结果当作一张表来读取，再在其上运行新的查询；这样既能对 SHOW/DESCRIBE/CALL 这类难以复用的结果做后处理，也能在分步调试一条复杂查询时，在已计算的中间结果之上叠加新的一层查询，而不必从头重新计算。
