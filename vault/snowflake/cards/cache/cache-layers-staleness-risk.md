---
id: cache-layers-staleness-risk
node: cache.cache-layer-tradeoffs
type: qa
tags: [grown]
---
## Q
传统的应用层缓存（例如 Redis 缓存查询结果）有返回陈旧数据的风险。Snowflake 的结果缓存、元数据缓存和仓库本地磁盘缓存各自有没有这种陈旧风险？

## A
三层都不会返回陈旧数据，因为它们都挂在不可变的微分区（micro-partition）之上。结果缓存只在底层表未发生变化时才会被复用；元数据统计随每次提交原子更新；本地磁盘缓存存的是按文件缓存的不可变分区，表更新后查询引用的是新分区文件，旧缓存只是用不上而不是读错。三层的差别在于命中率和预热成本，而不在正确性。
