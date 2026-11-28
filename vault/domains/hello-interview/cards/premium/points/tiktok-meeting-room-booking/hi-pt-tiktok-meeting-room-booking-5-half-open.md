---
id: hi-pt-tiktok-meeting-room-booking-5-half-open
node: qb.sd.tiktok-meeting-room-booking.points
type: qa
step: 5
---
## Q
**会议室预订系统 · 半开区间**｜必会 · 出自：会议室预订系统 › 核心实体与接口

10:00–11:00 的会议和 11:00–12:00 的会议在同一间房里算冲突吗？时间区间用什么约定，时间用什么时区存储？

## A
**约定。** 半开区间 `[start, end)`：两场会议可以相邻，不算冲突。重叠的判定是 `startA < endB 且 startB < endA`。

**时区。** 数据库存 UTC，每间房记录自己的时区，展示和重复会议展开时才换算。
