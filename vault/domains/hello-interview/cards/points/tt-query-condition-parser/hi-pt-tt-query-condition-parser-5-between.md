---
id: hi-pt-tt-query-condition-parser-5-between
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 5
---
## Q
**条件解析与内存表查询 · BETWEEN 里的 AND**｜出自：条件解析与内存表查询 › 完整实现 3

`age BETWEEN 18 AND 40 AND vip = 1` 里有两个 `AND`，解析器怎么区分？

## A
**要点。** 第一个 `AND` 属于 `BETWEEN` 语法，由 `predicate` 在读到 `BETWEEN` 后直接 `expect` 吃掉；第二个才回到 `and_expr` 的循环。

**写法。** 解析成 `And(Cmp(>=), Cmp(<=))`，不用新增节点。

**易错。** 如果用 `split` 或先切分 `AND`，这里一定错。
