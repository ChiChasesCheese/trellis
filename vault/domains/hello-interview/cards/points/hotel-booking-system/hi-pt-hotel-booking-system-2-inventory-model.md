---
id: hi-pt-hotel-booking-system-2-inventory-model
node: qb.sd.hotel-booking-system.points
type: qa
step: 2
---
## Q
**酒店预订系统 · 房型 × 日期的库存建模**｜必会 · 出自：酒店预订系统 › 深入 1

房态怎么存？每个房间每天一行、只存预订表算重叠、房型×日期计数行三种方案怎么比？

## A
**数字。** 10 万家酒店 × 20 个房型 × 365 天 = 7.3 亿行，每行约 50 字节共约 36 GB，可分片；每间房每天一行是 365 亿行，不可行。
**对比。** 只存预订表则每次搜索扫预订表。
**选择。** 房型×日期计数行，主键 `(hotel_id, room_type_id, date)`，字段 `total`、`reserved`、`price`、`version`。
**代价。** 无具体房号，需要时入住前再分配或另设 Room 表。
