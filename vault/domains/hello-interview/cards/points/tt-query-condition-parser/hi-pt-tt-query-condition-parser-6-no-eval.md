---
id: hi-pt-tt-query-condition-parser-6-no-eval
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 6
---
## Q
**条件解析与内存表查询 · 为什么不用 eval**｜出自：条件解析与内存表查询 › 深入 2

把条件字符串改写成 Python 表达式再 `eval`，代码很短。为什么不行？

## A
**要点。** 查询字符串不可信，`eval` 等于执行任意代码；也处理不了 `NULL` 三值逻辑和 `LIKE`。

**对比。** 语法树只有我们定义的节点，`name = 'x'; DROP TABLE users` 在词法这一步就报错。

**延伸。** 参数化查询（`age > ?`）把值和结构分开，从根上避免注入。
