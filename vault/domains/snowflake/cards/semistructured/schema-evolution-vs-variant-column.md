---
id: schema-evolution-vs-variant-column
node: semistructured.schema-evolution-tables
type: qa
tags: [grown]
---
## Q
应对不断新增字段的数据源，「开启表模式演进」和「把整条记录存进一个 VARIANT 列」各有什么取舍？

## A
VARIANT 列天然容纳任何新字段，不需要改表，但查询时要写路径表达式并做类型转换，下游用户看到的是半结构化数据。模式演进把新字段变成真正的有类型列，下游可以像普通表一样查询、授权和做列级治理；代价是表的列数会随上游不断增长，上游的临时字段或拼写错误也会变成永久的列。结构相对稳定、下游需要强类型列时选模式演进；字段高度多变时保留 VARIANT 更稳妥。
