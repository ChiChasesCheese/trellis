---
id: result-cache-invalidation-config-options
node: cache.result-cache-invalidation
type: qa
source: snowflake-docs
---
## Q
除了底层表数据发生变化之外，还有什么「看不见数据」的变化也会使一条已经缓存的查询结果失效？

## A
任何会影响结果如何被产生的配置选项一旦改变，就会使缓存失效——例如影响查询计算方式或格式的会话/账户参数设置发生了变化；即使 SQL 文本和表数据都完全相同，只要产生结果的「配方」变了，Snowflake 也不会复用旧的持久化结果，而是重新计算。
