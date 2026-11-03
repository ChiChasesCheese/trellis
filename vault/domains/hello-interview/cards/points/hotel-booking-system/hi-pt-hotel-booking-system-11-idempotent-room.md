---
id: hi-pt-hotel-booking-system-11-idempotent-room
node: qb.sd.hotel-booking-system.points
type: qa
step: 10
---
## Q
**酒店预订系统 · 重复点击与会议室缩小版**｜追问 · 出自：酒店预订系统 › 取舍与追问

追问：用户重复点击下单怎么办？会议室预订的缩小版怎么做？

## A
**重复点击。** 幂等键，唯一约束 `(user_id, 幂等键)`。
**会议室。** 房间数少，直接对 Room 表用区间排他约束（PostgreSQL 的 `EXCLUDE USING gist (room_id WITH =, daterange WITH &&)`），开始结束时间重叠即冲突，省去计数行。
