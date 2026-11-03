---
id: hi-pt-tt-query-condition-parser-3-lexer
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 3
---
## Q
**条件解析与内存表查询 · 为什么要先做词法分析**｜出自：条件解析与内存表查询 › 完整实现 1

解析 `name = 'A AND B' OR age > 3`，为什么不能直接按 `AND`、`OR` 做字符串 `split`？

## A
**要点。** `split` 分不清字符串里的 `AND` 和运算符 `AND`，也处理不了括号。词法先把引号里的内容整体变成一个值 token。

**易错。** 字符串里的单引号写成两个单引号 `'O''Neil'`；关键字不分大小写，字段名区分。
