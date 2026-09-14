---
id: result-cache-invalidation-reclustering
node: cache.result-cache-invalidation
type: qa
source: snowflake-docs
---
## Q
一张表里的每一行数据的值都没有发生任何变化，但后台的自动重新聚簇（automatic reclustering）或分区合并（consolidation）重写了这张表的微分区文件，此时此前对这张表的持久化查询结果缓存还能被命中吗？为什么？

## A
不能。结果缓存判断数据是否变化，看的是表当前依赖的微分区文件集合是否与生成缓存结果时的集合一致，而不是逐行比较数据值；重新聚簇或合并会用新的微分区文件替换旧的，即便行内容在逻辑上完全相同，底层文件已经不同，所以会使该表相关的缓存结果失效，下一次查询必须重新计算。
