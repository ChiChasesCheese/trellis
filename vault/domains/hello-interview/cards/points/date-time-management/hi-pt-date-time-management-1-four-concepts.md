---
id: hi-pt-date-time-management-1-four-concepts
node: qb.lld.date-time-management.points
type: qa
step: 1
---
## Q
**日期时间库 · 必须分开的四个概念**｜必会 · 出自：日期时间库 › 深入 1

设计日期时间库时，最大的设计原则是把哪四个常被混在一起的概念分开？绝大多数日期时间 bug 的根源是什么？

## A
**要点。** 时间线上的一个点（Instant）、墙上的钟表读数（LocalDateTime，没有时区）、时区规则（偏移量随日期变化）、时间的量（精确时长 Duration 与日历时长 Period）。全部做成不可变值对象。
**易错。** 绝大多数 bug 来自把它们混为一谈，例如把没有时区的读数当成时间点去比较先后。
