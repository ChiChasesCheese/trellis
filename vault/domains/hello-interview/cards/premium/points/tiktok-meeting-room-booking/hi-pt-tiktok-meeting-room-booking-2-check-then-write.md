---
id: hi-pt-tiktok-meeting-room-booking-2-check-then-write
node: qb.sd.tiktok-meeting-room-booking.points
type: qa
step: 2
---
## Q
**会议室预订系统 · 先查后写为什么会双订**｜必会 · 出自：会议室预订系统 › 深入 1

预订接口先查询该房间该时段是否空闲，空闲再插入。并发下会出什么问题？

## A
**问题。** 两个请求同时查到空闲，都去写，都成功，房间被双订。

**要点。** 不重叠必须由数据库保证，不能靠应用的先查后写。搜索结果只是建议，最终以带约束的写入为准。
