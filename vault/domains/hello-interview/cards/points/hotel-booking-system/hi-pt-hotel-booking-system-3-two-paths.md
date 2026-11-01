---
id: hi-pt-hotel-booking-system-3-two-paths
node: qb.sd.hotel-booking-system.points
type: qa
step: 3
---
## Q
**酒店预订系统 · 搜索路径与下单路径**｜出自：酒店预订系统 › 整体设计

搜索和下单为什么走两条不同的路径？搜索怎么查到某日期范围内有房的酒店？

## A
**搜索（读）。** Elasticsearch 按城市、设施、评分得几百个候选，再批量查预聚合表 `availability_summary(hotel_id, date, min_price, rooms_left)`（Redis 或只读副本）过滤排序；摘要由库存变更事件异步刷新，允许几十秒到分钟的过期。
**下单（写）。** 对房型库存行原子扣减，建 HELD 预订，库存库按 `hotel_id` 分片，事务不跨分片。
**为什么。** 写库扛不住 3 万次/秒的跨酒店聚合。
