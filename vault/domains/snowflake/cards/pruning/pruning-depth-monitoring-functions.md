---
id: pruning-depth-monitoring-functions
node: pruning.clustering-depth-metric
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 里，用什么系统函数可以查看一张表当前的聚簇深度，以及更完整的聚簇元数据（比如微分区总数、有重叠的微分区数量）？

## A
`SYSTEM$CLUSTERING_DEPTH` 用于直接返回某张表（在指定列上）的聚簇深度数值；`SYSTEM$CLUSTERING_INFORMATION` 返回更完整的聚簇元数据，包括聚簇深度、微分区总数、以及有重叠的微分区数量等，可以用它们来监控大表的聚簇“健康状况”，尤其是在持续有 DML 写入的情况下随时间跟踪变化。
