---
id: hi-pt-tt-query-condition-parser-11-relational-vs-doc
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 11
---
## Q
**条件解析与内存表查询 · 关系表和文档差在哪**｜出自：条件解析与内存表查询 › 深入 5

同一套解析器，要同时支持关系表和 NoSQL 文档。哪些地方不同？

## A
**要点。** 解析和求值完全一样，只差存储层：

| 方面 | 关系型 | 文档型 |
|---|---|---|
| 字段 | `columns` 校验 | `columns=None` |
| 未知字段 | 报错 | 当作 `NULL` |
| 嵌套 | 无 | 点路径 `address.city` |
| 类型不匹配 | 建表可拦 | 当不匹配 |
