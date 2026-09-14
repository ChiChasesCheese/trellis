---
id: attrib-warehouse-to-query
node: cost.access-history-lineage-for-cost
type: qa
tags: [grown]
---
## Q
`WAREHOUSE_METERING_HISTORY` 只给出每个仓库每小时消耗的信用点。怎样把仓库的信用点进一步分摊到单条查询上？分摊后为什么总和小于仓库账单？

## A
使用 ACCOUNT_USAGE 的 `QUERY_ATTRIBUTION_HISTORY` 视图，它为每条查询给出归属于该查询的仓库计算信用点（多条并发查询按资源使用分摊），可再按 `QUERY_HASH`/参数化哈希、用户、`QUERY_TAG` 聚合出最贵的查询模式。它的总和通常小于仓库计量，因为仓库在没有查询时的空转时间不归属于任何查询，云服务、无服务器等费用也不在其中；两者的差额正是空转成本，本身就是一个优化信号（自动挂起设置过长）。
