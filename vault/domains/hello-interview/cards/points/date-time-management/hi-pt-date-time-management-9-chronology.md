---
id: hi-pt-date-time-management-9-chronology
node: qb.lld.date-time-management.points
type: qa
step: 10
---
## Q
**日期时间库 · 日历系统抽象**｜加分 · 出自：日期时间库 › 深入 8

库要支持公历、农历、伊斯兰历等多种日历。日期类应该怎样设计，才能让跨日历转换和星期计算自然成立？

## A
**要点。** 把"纪元日 ↔ 年月日"抽成 Chronology 策略，各日历一个实现；LocalDate 保存纪元日，不依赖具体日历。
**结果。** 跨日历转换先转纪元日再用目标日历展开；星期几、两日期相差天数只依赖纪元日，所有日历共用。
