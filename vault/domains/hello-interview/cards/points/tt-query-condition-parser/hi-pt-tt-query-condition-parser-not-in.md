---
id: hi-pt-tt-query-condition-parser-not-in
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 7
---
## Q
**条件解析与内存表查询 · NOT 和 IN 怎么加**｜追问 · 出自：条件解析与内存表查询 › 逐步扩展 1

第一版只有比较、`AND`、`OR`。要加 `NOT` 和 `IN`，改哪里？

## A
**要点。** `NOT` 优先级高于 `AND`，在 `and_expr` 和 `primary` 之间加一层 `not_expr`，再加 `Not` 节点。`IN` 在比较部分加分支，读括号里的值列表，再加 `In` 节点。

**为什么容易。** 语法树和表都不用改，这就是分层的好处。
