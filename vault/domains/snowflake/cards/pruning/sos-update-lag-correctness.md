---
id: sos-update-lag-correctness
node: pruning.search-optimization-service
type: qa
source: snowflake-docs
---
## Q
当表的数据被加载或做了 DML 更新之后，如果这时候恰好有查询在跑，而搜索访问路径还没更新完，查询结果会不会因此出错？会有什么副作用？

## A
不会出错：维护服务会自动把新数据的变更同步更新到搜索访问路径里，即使查询恰好在更新过程中执行，也始终返回正确结果。唯一的副作用是性能上的——在搜索访问路径还没跟上最新数据变化之前运行的查询，加速效果会打折扣、可能跑得比访问路径已同步时慢。
