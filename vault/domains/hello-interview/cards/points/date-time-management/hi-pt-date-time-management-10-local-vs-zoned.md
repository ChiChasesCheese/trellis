---
id: hi-pt-date-time-management-10-local-vs-zoned
node: qb.lld.date-time-management.points
type: qa
step: 2
---
## Q
**日期时间库 · LocalDateTime 与 ZonedDateTime 的区别**｜必会 · 出自：日期时间库 › 深入 1

LocalDateTime 和 ZonedDateTime 有什么区别？时区转换接口为什么要提供两个不同的方法？

## A
**区别。** 前者只是读数，没有对应时间点，不能直接比较先后，也不能转 UTC；后者带时区，才对应唯一时间点。混用是最常见的 bug 来源。
**接口。** `with_zone(other)` 保持时间点不变，只改展示；`with_local_same(other)` 保持墙钟读数不变，改变时间点。语义易混，用不同方法名。
