---
id: hi-pt-tiktok-meeting-room-booking-9-timezone-dst
node: qb.sd.tiktok-meeting-room-booking.points
type: qa
step: 9
---
## Q
**会议室预订系统 · 时区与夏令时**｜追问 · 出自：会议室预订系统 › 深入 5

重复会议跨越夏令时切换，“每周一 10 点”应该怎么展开？为什么不能每隔 7 天相加？

## A
**要点。** 按房间所在地的本地时间展开：夏令时前后同一个“周一 10 点”对应的 UTC 不同。

**易错。** 若直接在 UTC 上每次加 7 天，切换夏令时后会议会漂移一小时。展开时才换算，数据库里只存 UTC。
