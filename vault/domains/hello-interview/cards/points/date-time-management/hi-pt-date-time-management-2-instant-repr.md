---
id: hi-pt-date-time-management-2-instant-repr
node: qb.lld.date-time-management.points
type: qa
step: 2
---
## Q
**日期时间库 · Instant 为什么不用单个纳秒整数**｜出自：日期时间库 › 核心实体与接口

日期时间库里 Instant 表示时间线上的一个点。能不能只用一个 64 位纳秒整数存"自纪元起的纳秒"？应该怎么存？

## A
**问题。** 64 位纳秒整数只覆盖 1970 年前后约 292 年（约 1677 到 2262 年），范围不够。
**做法。** 秒和纳秒分开存，即自纪元起的秒加纳秒。
**对比。** LocalDate 只存一个整数：自 1970-01-01 起的天数（纪元日）；LocalTime 存当天的纳秒数。
