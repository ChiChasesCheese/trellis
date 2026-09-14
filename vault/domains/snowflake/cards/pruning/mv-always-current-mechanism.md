---
id: mv-always-current-mechanism
node: pruning.materialized-views-maintenance
type: qa
source: snowflake-docs
---
## Q
Snowflake 的物化视图（materialized view）由后台服务异步刷新。如果基表刚做完 DML、物化视图还没刷新，这时查询它会不会读到过期数据？为什么？

## A
不会。通过物化视图访问的数据始终是最新的：若查询在刷新完成前到达，Snowflake 要么先把物化视图更新，要么使用物化视图中仍然有效的部分，再从基表读取变化过的较新数据补齐。代价只体现在性能上（需要回基表读一部分），而非正确性上。
