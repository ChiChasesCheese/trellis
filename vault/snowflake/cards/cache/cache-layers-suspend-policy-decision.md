---
id: cache-layers-suspend-policy-decision
node: cache.cache-layer-tradeoffs
type: qa
tags: [grown]
---
## Q
一个仪表盘每隔几分钟就发起一批互不相同但扫描同一张大表的查询。若想降低延迟，调整自动挂起（auto-suspend）时长和依赖结果缓存，哪个更有效？

## A
调整自动挂起更有效。这些查询 SQL 各不相同，结果缓存（result cache，只复用完全相同查询的结果）几乎无法命中；而它们读取的是同一批微分区，正是仓库本地磁盘缓存（warehouse local disk cache）能帮上忙的场景。把 auto-suspend 设得比查询间隔更长，仓库不挂起、缓存保持热态，代价是空闲时间也要按秒计费。
