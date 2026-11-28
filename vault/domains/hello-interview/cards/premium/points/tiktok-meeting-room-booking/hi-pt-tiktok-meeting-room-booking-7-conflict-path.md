---
id: hi-pt-tiktok-meeting-room-booking-7-conflict-path
node: qb.sd.tiktok-meeting-room-booking.points
type: qa
step: 7
---
## Q
**会议室预订系统 · 冲突是正常路径**｜必会 · 出自：会议室预订系统 › 深入 3

用户点“预订”时，房间已被别人刚订走，插入因约束失败。接口应该怎么表现？自动选房怎么重试？

## A
**表现。** 返回 409 并附前 3 个替代方案（附近时段、邻近房间），不让用户看到“系统错误”。

**自动选房。** 服务端最多重试 3 次，每次换下一个候选。

**幂等。** `Idempotency-Key` 唯一约束，手机上点两次不会订两间。
