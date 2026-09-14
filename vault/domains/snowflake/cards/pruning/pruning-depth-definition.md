---
id: pruning-depth-definition
node: pruning.clustering-depth-metric
type: qa
source: snowflake-docs
---
## Q
聚簇深度（clustering depth）这个指标衡量的是什么？它的取值范围是怎样的，空表的聚簇深度是多少？

## A
聚簇深度衡量的是：对于指定的一组列，一张表里相互重叠（即取值范围有交集）的微分区（micro-partition）的平均重叠层数。取值为 1 或更大的整数（含小数平均值），数值越小说明表在这些列上聚簇得越好。一张没有任何微分区的空表，聚簇深度定义为 0。
