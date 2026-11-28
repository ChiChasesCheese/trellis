---
id: hi-pt-tiktok-meeting-room-booking-3-exclusion-constraint
node: qb.sd.tiktok-meeting-room-booking.points
type: qa
step: 3
---
## Q
**会议室预订系统 · 排除约束防重叠**｜必会 · 出自：会议室预订系统 › 深入 1

在 Postgres 里怎样让数据库直接拒绝同一房间的重叠预订？取消的预订怎么处理？

## A
**要点。** 排除约束：`EXCLUDE USING gist (room_id WITH =, tstzrange(start_ts, end_ts, '[)') WITH &&) WHERE (status = 'CONFIRMED')`。`room_id WITH =` 这类等值条件需要先启用 `btree_gist` 扩展。同一房间区间重叠时插入报错，并发安全由数据库内部加锁保证。

**取消。** 把状态改成 CANCELLED，不再参与约束。
