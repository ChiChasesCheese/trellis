---
id: hi-pt-tiktok-meeting-room-booking-10-no-show
node: qb.sd.tiktok-meeting-room-booking.points
type: qa
step: 10
---
## Q
**会议室预订系统 · 未到场自动释放**｜追问 · 出自：会议室预订系统 › 深入 6

有人订了房间却不来，怎么把它释放给别人？

## A
**要点。** 签到（扫码或会议室平板）。开始后 10 分钟无人签到，定时任务把预订改为 CANCELLED 并释放，同时通知组织者。

**实现。** 任务靠 `start_ts` 上的索引扫描，数据量小，不需要复杂的调度。
