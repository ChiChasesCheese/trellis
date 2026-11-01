---
id: hi-pt-flight-search-system-4-single-flight
node: qb.sd.flight-search-system.points
type: qa
step: 4
---
## Q
**机票搜索系统 · 请求合并**｜出自：机票搜索系统 › 整体设计

热门航线开售瞬间，大量用户搜同一个键，怎么避免账单变成 N 倍？

## A
**要点。** 请求合并（single-flight）：同一搜索键同时到达的多个请求只放行一个去调供应商，其余订阅这个飞行中的结果；用分布式租约或 Redis 占位键实现。
