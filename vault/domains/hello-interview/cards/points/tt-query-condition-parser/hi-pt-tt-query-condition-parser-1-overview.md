---
id: hi-pt-tt-query-condition-parser-1-overview
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 1
---
## Q
**条件解析与内存表查询 · 整体分几层**｜出自：条件解析与内存表查询 › 需求

给一个 SQL 风格的查询字符串，要在内存表上执行。代码应该分成哪几层，每层的输入输出是什么？

## A
**要点。** 四层：`tokenize`（字符串 → token）→ `Parser`（token → 语法树 AST）→ 节点 `eval(row)`（语法树 + 一行 → 真假）→ `Table`（存行、索引、排序、投影）。

**为什么。** 解析和存储分开，换存储（关系表、文档）不用改解析；加运算符只加一个节点类。
