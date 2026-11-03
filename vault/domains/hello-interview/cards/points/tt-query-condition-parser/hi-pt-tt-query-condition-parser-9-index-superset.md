---
id: hi-pt-tt-query-condition-parser-9-index-superset
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 9
---
## Q
**条件解析与内存表查询 · 索引不能漏行的不变量**｜出自：条件解析与内存表查询 › 深入 4

`WHERE city = 'NYC' AND age > 18` 和 `WHERE city = 'NYC' OR age > 18`，`city` 有哈希索引，`age` 没有。分别怎么用索引？

## A
**要点。** 不变量：候选集必须是真实结果的超集，最后再用条件复查。

**AND。** 用 `city` 的候选集，再复查 `age`。

**OR。** 不能用索引：`age > 18` 的行可能不在 `city` 候选集里，只能全表扫描。

**数字。** 两边都有索引时：`AND` 取交集，`OR` 取并集。
