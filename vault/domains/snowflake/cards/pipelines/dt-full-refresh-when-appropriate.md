---
id: dt-full-refresh-when-appropriate
node: pipelines.dynamictable-incremental-vs-full-refresh
type: qa
source: snowflake-docs
---
## Q
什么情况下显式选择全量刷新（FULL）反而是合理的？

## A
1) 查询定义无法增量计算时，只能全量；2) 源表很小，每次重算的成本本就很低，增量带来的节省有限；3) 每次刷新之间基表的大部分数据都会变化，此时计算增量并不比重新计算整个结果便宜。全量刷新的代价是工作量随结果集规模增长，并且每次都会替换大量微分区，存储和计算开销都会随表增大而上升。
