---
id: hi-pt-tt-query-condition-parser-lexer
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 3
---
## Q
**条件解析与内存表查询 · 为什么要先做词法**｜必会 · 出自：条件解析与内存表查询 › 核心实现 1

解析 `name = 'A AND B' OR age > 3`，为什么不能按 `AND`、`OR` 做 `split`？

## A
**要点。** `split` 分不清字符串里的 `AND` 和运算符 `AND`，也处理不了括号。词法把引号里的内容整体变成一个 token。

**易错。** 正则里长运算符写在前面，否则 `<=` 会切成 `<` 和 `=`。
