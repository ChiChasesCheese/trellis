---
id: hi-pt-tiktok-meeting-room-booking-6-search-best-fit
node: qb.sd.tiktok-meeting-room-booking.points
type: qa
step: 6
---
## Q
**会议室预订系统 · 搜索与自动选房**｜必会 · 出自：会议室预订系统 › 深入 2

用户只给出人数、设备和时间，让系统自动选房。搜索怎么写，选哪一间？

## A
**搜索。** 在一栋楼的约 100 间房里找 `NOT EXISTS`（同房间、已确认、时间区间重叠的预订），GiST 索引支持，毫秒级。

**选房。** 先满足人数和设备，选容量最小的（best fit）；同等条件下选当天已有预订最少或能“紧挨”相邻预订的房间，避免把空闲时间切碎。
