---
id: hi-pt-tt-query-condition-parser-index-superset
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 9
---
## Q
**条件解析与内存表查询 · 索引为什么 OR 用不了**｜追问 · 出自：条件解析与内存表查询 › 逐步扩展 3

`city` 有哈希索引，`age` 没有。`city = 'NYC' AND age > 18` 和 `city = 'NYC' OR age > 18` 分别怎么查？

## A
**要点。** 不变量：候选集必须是结果的超集，最后复查。

**AND。** 用 `city` 的候选集，再复查 `age`。

**OR。** `age > 18` 的行可能不在 `city` 候选集里，用索引会漏行，只能全表扫描。
