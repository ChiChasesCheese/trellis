---
id: hi-sd-ticketmaster-11-search-cache
node: sd.problem-breakdowns.ticketmaster
type: qa
step: 11
---
## Q
**加速重复搜索：查询缓存与边缘缓存**｜系统设计 · 问题拆解

对频繁重复的搜索查询，缓存键怎么设计、有哪几层缓存、有什么前提和难点？

## A
**应用缓存（Redis / Memcached）。** 缓存键要包含所有会改变结果的搜索参数，如 `search:keyword=Taylor Swift&start=...&end=...`；设合适的 TTL（如 24 小时）。难点：失效，尤其是模糊搜索结果；用 TTL 加基于缓存标签的失效触发来折中。缓存未命中多时，高峰仍压到搜索层。

**引擎内置缓存。** Elasticsearch 在分片级有用于过滤结果的查询缓存，以及缓存整个搜索响应的请求缓存（适合聚合多的查询），可以学习并缓存最常见的查询。

**CDN 边缘缓存。** 如 CloudFront，把结果缓存到离用户近处。前提：结果不个性化，同一查询对所有人相同。

**难点。** 搜索查询与结果之间没有显式关联，新活动上线时很难精准失效；需要更多基础设施。
