---
id: hi-pt-tt-query-condition-parser-overview
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 2
---
## Q
**条件解析与内存表查询 · 分几层**｜必会 · 出自：条件解析与内存表查询 › 整体设计

条件字符串到查询结果，代码分哪几层？每层的输入输出是什么？

## A
**要点。** `tokenize`（字符串 → token）→ `Parser`（token → 语法树）→ `matches(row)`（语法树 + 一行 → 真假）→ `Table`（存行、过滤）。

**为什么。** 解析和存储分开：换存储不改解析，加运算符不改表。
