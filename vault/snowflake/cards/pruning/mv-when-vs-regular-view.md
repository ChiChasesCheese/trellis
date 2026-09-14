---
id: mv-when-vs-regular-view
node: pruning.materialized-views-maintenance
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 里，面对一条耗资源的视图查询，什么条件下该建物化视图（materialized view，预先计算并存储结果的视图），什么条件下只建普通视图就够了？

## A
三个条件同时成立才值得物化：结果不常变（基表或视图用到的那部分行很少变化）、结果被使用的频率远高于其变化频率、查询本身很耗资源（算力、信用点或中间结果存储）。只要结果频繁变化、使用不频繁，或查询本身不贵，就用普通视图。原因是物化视图的存储和后台自动维护都要花钱，只有复用次数足够多才能抵消这笔持续成本。
