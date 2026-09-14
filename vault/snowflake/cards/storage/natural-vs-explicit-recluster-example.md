---
id: natural-vs-explicit-recluster-example
node: storage.natural-vs-explicit-clustering
type: qa
source: snowflake-docs
---
## Q
一张表自然按 `date` 分布在微分区 1–4 中，某查询要扫描 1、2、3 三个分区。定义聚簇键 `(date, type)` 并重新聚簇后发生了什么？

## A
重新聚簇会按聚簇键重组数据，生成新的微分区 5–8，同一查询只需扫描分区 5。分区 5 达到恒定状态（constant state，无法再通过聚簇改进），今后计算深度和重叠时会被排除；原来的分区 1–4 被标记为已删除但不会立刻清除，而是为 Time Travel（时间旅行）和 Fail-safe（故障保护）保留。表越大（数百万分区），这种扫描量的缩减越显著。
