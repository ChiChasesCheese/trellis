---
id: hi-pt-tt-query-condition-parser-no-eval
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 6
---
## Q
**条件解析与内存表查询 · 为什么不用 eval**｜必会 · 出自：条件解析与内存表查询 › 需求

把条件改写成 Python 表达式再 `eval`，代码很短。为什么不行？

## A
**要点。** 查询字符串不可信，`eval` 等于执行任意代码；也处理不了 `NULL` 语义。语法树只有我们定义的节点，非法内容在词法或语法这一步就报错。
