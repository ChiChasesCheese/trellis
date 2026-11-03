---
id: hi-pt-tt-query-condition-parser-order-by
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 11
---
## Q
**条件解析与内存表查询 · ORDER BY 遇到 NULL**｜加分 · 出自：条件解析与内存表查询 › 取舍与追问

`rows.sort(key=lambda r: r[field])` 在有 `NULL` 的列上会怎样？怎么改？

## A
**要点。** `None < 3` 抛 `TypeError`。排序键用元组 `(v is not None, 0 if v is None else v)`，`NULL` 排最小。

**易错。** 写成 `v or 0` 会把空字符串变成 `0`，和字符串比较时报错。
