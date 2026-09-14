---
id: profile-pruning-scanned-vs-total
node: query.reading-query-profile
type: qa
source: snowflake-docs
---
## Q
如何在查询画像（Query Profile）里判断一张表的剪枝（pruning）是否有效？如果剪枝没效果但上方有 Filter 算子过滤掉大量行，说明什么？

## A
看 TableScan 算子的 Pruning 统计：比较 `Partitions scanned`（已扫描分区数）与 `Partitions total`（表总分区数）。前者只占后者很小比例，说明剪枝有效；接近总数则说明剪枝没起作用。若剪枝没减少数据，而 TableScan 上方的 Filter 算子又过滤掉了大量记录，说明数据的存储顺序与查询过滤条件不相关，换一种数据组织方式（例如按过滤列聚簇）可能会让这个查询受益。
