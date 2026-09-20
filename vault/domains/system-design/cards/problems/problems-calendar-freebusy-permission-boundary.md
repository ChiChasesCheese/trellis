---
id: problems-calendar-freebusy-permission-boundary
node: problems.realtime.calendar
type: qa
step: 5
tags: [grown]
---
## Q
A calendar system's free/busy query for multiple attendees should return only busy/free intervals, never full event details, and should run against a per-user range index of busy intervals rather than scanning each attendee's full event table. Why does CalDAV (RFC 4791) treat this as a deliberate protocol-level distinction rather than an implementation detail?

## A
CalDAV defines two separate REPORT methods with different permission scopes: `calendar-query` returns full event data (subject to normal access control), while `free-busy-query` returns only availability intervals, deliberately allowing a requester to check whether someone is free without being able to see what they're busy with. Treating this as a protocol-level distinction — not just an internal optimization — means a system that only implements the range-index performance optimization but still leaks event titles through the free/busy response has broken the actual privacy boundary the protocol was designed to enforce, not just taken a slower implementation path.

## Q zh
日历系统对多个参会人的 free/busy 查询应该只返回忙闲区间，绝不返回完整事件详情，而且应该针对每个用户的忙碌区间范围索引运行，而不是扫描每个参会人的完整事件表。为什么 CalDAV（RFC 4791）把这当作一个刻意的协议层区分，而不只是一个实现细节？

## A zh
CalDAV 定义了两个权限范围不同的独立 REPORT 方法：`calendar-query` 返回完整事件数据（受正常访问控制约束），而 `free-busy-query` 只返回可用性区间，刻意允许请求方在看不到对方具体在忙什么的前提下,查询对方是否有空。把这当作协议层的区分——而不只是内部性能优化——意味着一个只实现了范围索引这一性能优化、却仍然通过 free/busy 响应泄露了事件标题的系统，破坏的是协议本来要强制执行的实际隐私边界，而不只是选了一条较慢的实现路径。
