---
id: problems-hotel-reservation-search-index-vs-booking-path
node: problems.commerce.hotel-reservation
type: qa
step: 6
tags: [grown]
---
## Q
Why does a hotel/marketplace search system serve results from a denormalized, minutes-stale index rather than querying the authoritative per-night inventory table directly for every search request?

## A
Computing precise per-night availability and price for every candidate listing is expensive and combinatorially explodes with the number of nights and candidates — a single mid-size destination can have 10,000+ properties, and pricing all of them on every search would make search compete with booking for the same database connections and buffer pool. Instead the system runs two stages: a fast candidate-generation query against a denormalized index (coarse price range, rough availability flag, refreshed asynchronously) narrows millions of listings to the handful a user will actually view, and only those listings get a precise, authoritative availability+price query against the real inventory table — keeping the expensive per-night computation off the critical path for every search.

## Q zh
为什么酒店/民宿搜索系统用一份反规范化的、允许有几分钟延迟的索引来返回结果，而不是每次搜索都直接查权威的按夜库存表？

## A zh
为每一个候选房源精确计算逐晚可用性和价格代价很高，而且会随晚数和候选数产生组合爆炸——一个中等城市目的地就可能有一万多个房源，如果每次搜索都对全部候选做精确定价，搜索会和预订争抢同一批数据库连接和缓冲池。系统改用两阶段：先对一份反规范化索引（粗粒度价格区间、粗略可订标记，异步刷新）做快速候选生成，把上百万房源收窄到用户实际会看的一小撮；只有这些被点开的房源才触发对真实库存表的精确、权威的可用性+价格查询——把昂贵的逐晚计算挡在每次搜索的关键路径之外。
