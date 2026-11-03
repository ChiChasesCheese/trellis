---
id: hi-pt-date-time-management-6-duration-period
node: qb.lld.date-time-management.points
type: qa
step: 7
---
## Q
**日期时间库 · Duration 与 Period 为何分开**｜追问 · 出自：日期时间库 › 深入 4

夏令时当天只有 23 或 25 小时。2024 年 3 月 9 日中午加"1 天"和加"24 小时"，结果有何不同？库为什么要把 Duration 和 Period 分开？

## A
**例子。** 春季拨快当天只有 23 小时：加 Period 一天得到 3 月 10 日中午，实际过了 23 小时；加 Duration 24 小时得到 3 月 10 日 13:00。
**语义。** "明天同一时间开会"用日历天，"24 小时后到期"用精确时长。
**实现。** `plus_days` 在墙钟上加再重新解析偏移；`plus(Duration)` 在时间线上加。
