---
id: dt-incremental-why-cheaper
node: pipelines.dynamictable-incremental-vs-full-refresh
type: qa
source: snowflake-docs
---
## Q
基表每天新增 1% 的数据。一张基于它的动态表用增量刷新和全量刷新，每次刷新的工作量有何本质区别？

## A
每次刷新时，Snowflake 先检测基表发生了变化。增量刷新（INCREMENTAL）只计算发生变化的行，工作量大致与变化量（这里约 1%）成正比；全量刷新（FULL）则重新计算整个结果集，工作量与全表规模成正比，与变化多少无关。无论哪种模式，新结果都原子地应用到动态表上。基表大、变化比例小时，增量刷新能显著节省仓库计算。
