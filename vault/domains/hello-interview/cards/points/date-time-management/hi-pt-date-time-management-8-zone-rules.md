---
id: hi-pt-date-time-management-8-zone-rules
node: qb.lld.date-time-management.points
type: qa
step: 8
---
## Q
**日期时间库 · 时区规则存储与未来事件**｜出自：日期时间库 › 深入 4

时区规则会被政府更新。库内部怎样存规则并查偏移量？数据库里存未来事件应该存什么，已发生的事件呢？

## A
**存储。** 按时间排序的转换点列表，二分查找某 UTC 时刻的偏移，O(log n)；未来规则（如三月第二个星期日）按年份惰性展开。偏移量由 ZoneRules 现算，不存在 ZonedDateTime 里。
**未来事件。** 存"本地时间 + 时区名"，只存 UTC 会在规则变化后让墙钟时间出错。
**已发生。** 存 UTC 就够了。
