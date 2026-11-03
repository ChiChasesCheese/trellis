---
id: hi-pt-tt-query-condition-parser-null-logic
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 8
---
## Q
**条件解析与内存表查询 · NULL 的三值逻辑**｜追问 · 出自：条件解析与内存表查询 › 逐步扩展 2

`age` 是 `NULL` 的行，`age >= 18` 和 `NOT age >= 18` 分别返回吗？

## A
**要点。** 都不返回：比较结果是「未知」，`NOT 未知` 还是未知，`WHERE` 只留 `True`。

**实现。** `matches` 返回 `True / False / None`，`select` 用 `is True` 过滤。

**规则。** `False AND 未知 = False`；`True OR 未知 = True`；其余有未知就是未知。
