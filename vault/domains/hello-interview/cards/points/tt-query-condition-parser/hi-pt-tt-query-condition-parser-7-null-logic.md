---
id: hi-pt-tt-query-condition-parser-7-null-logic
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 7
---
## Q
**条件解析与内存表查询 · NULL 的三值逻辑**｜出自：条件解析与内存表查询 › 深入 3

`age` 是 `NULL` 的行，`age >= 18` 和 `NOT age >= 18` 分别返回吗？`IS NULL` 呢？

## A
**要点。** 两个都不返回：比较结果是「未知」，`NOT 未知` 还是未知，`WHERE` 只留 `True`。只有 `age IS NULL` 会返回。

**实现。** `eval` 返回 `True / False / None`。

**短路。** `False AND 未知 = False`；`True OR 未知 = True`；其余有未知就是未知。

**易错。** 把 `None` 当 `False`，`NOT` 就会多返回 `NULL` 行。
