---
id: mv-automatic-query-rewrite
node: pruning.materialized-views-maintenance
type: qa
source: snowflake-docs
---
## Q
用户的 SQL 只查询基表、从未提到物化视图（materialized view），Snowflake 还可能用上它吗？优化器在什么情况下反而不用它？

## A
可能。优化器会自动改写（automatic query rewrite）针对基表或普通视图的查询，只要物化视图包含所需的全部行列（包括过滤条件被视图定义的过滤所“包含”（subsumption），如查询范围落在视图的 `BETWEEN` 范围内），就可改用它；被选用时 EXPLAIN 或 Query Profile 中显示的是物化视图而非基表。但如果基表按相关字段聚簇、能高效剪枝，优化器可能认为直接扫基表性能相当而不用物化视图。另外，候选物化视图变多会让编译阶段考虑更多方案，编译时间和资源也会增加。
