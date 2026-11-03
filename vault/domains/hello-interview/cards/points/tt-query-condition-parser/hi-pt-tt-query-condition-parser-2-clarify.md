---
id: hi-pt-tt-query-condition-parser-2-clarify
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 2
---
## Q
**条件解析与内存表查询 · 先问清楚什么**｜出自：条件解析与内存表查询 › 需求

面试官只说「解析一个条件，然后查表」。动手之前要问哪些问题？

## A
**要点。** 输入是完整 `SELECT` 还是只有条件；支持哪些运算符和括号；字段固定还是可嵌套（关系型还是 NoSQL）；值有没有 `NULL`；数据量、要不要索引；语法错误抛异常还是返回空。

**为什么。** 这几个答案决定文法、存储结构和 `NULL` 语义。
