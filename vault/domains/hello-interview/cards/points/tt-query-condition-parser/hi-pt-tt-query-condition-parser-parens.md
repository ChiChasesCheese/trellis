---
id: hi-pt-tt-query-condition-parser-parens
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 5
---
## Q
**条件解析与内存表查询 · 括号怎么处理**｜必会 · 出自：条件解析与内存表查询 › 核心实现 3

`(a = 1 OR b = 2) AND c = 3` 的括号在解析器里怎么实现？

## A
**要点。** 在最深的 `primary` 遇到 `(`，就回到最低优先级的 `or_expr` 解析里面的内容，再要求下一个 token 是 `)`。

**易错。** 解析完要检查没有多余 token，否则 `a > 1 b` 不会报错。
