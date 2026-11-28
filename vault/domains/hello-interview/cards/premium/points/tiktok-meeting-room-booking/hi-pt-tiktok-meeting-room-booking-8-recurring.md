---
id: hi-pt-tiktok-meeting-room-booking-8-recurring
node: qb.sd.tiktok-meeting-room-booking.points
type: qa
step: 8
---
## Q
**会议室预订系统 · 重复会议**｜追问 · 出自：会议室预订系统 › 深入 4

每周一 10 点的例会持续半年，怎么存？其中一周冲突了怎么办？

## A
**存法。** 存规则（RRULE）加物化实例：创建时生成未来 90 天内的每一场，各占一行，受约束保护；定时任务每天补齐新窗口。

**冲突。** 整个系列在一个事务里一起失败，并告诉用户具体哪几周冲突。单次修改是对实例的例外，“此场及以后”把系列拆成两段。
