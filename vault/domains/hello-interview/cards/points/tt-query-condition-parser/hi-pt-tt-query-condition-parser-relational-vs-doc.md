---
id: hi-pt-tt-query-condition-parser-relational-vs-doc
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 10
---
## Q
**条件解析与内存表查询 · 关系表和文档差在哪**｜追问 · 出自：条件解析与内存表查询 › 逐步扩展 4

同一套解析器要支持关系表和 NoSQL 文档，哪里不同？

## A
**要点。** 解析和求值一样，只差取字段：

| 方面 | 关系型 | 文档型 |
|---|---|---|
| 字段 | 校验 | 不校验 |
| 缺字段 | 报错 | 当 `NULL` |
| 嵌套 | 无 | `address.city` |
