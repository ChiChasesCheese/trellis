---
id: hi-pt-tt-query-condition-parser-clarify
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 1
---
## Q
**条件解析与内存表查询 · 先问清楚什么**｜必会 · 出自：条件解析与内存表查询 › 需求

面试官只说「解析一个条件，然后查表」。动手之前问什么？第一版约定什么？

## A
**要点。** 只有条件还是完整 `SELECT`；值的类型；有没有 `NULL`；字段固定吗；语法错误怎么处理。

**第一版。** 只有条件，整数和字符串，没有 `NULL`，字段固定，错误抛 `ValueError`。
