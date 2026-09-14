---
id: pruning-depth-overlap-hurts-pruning
node: pruning.clustering-depth-metric
type: qa
source: snowflake-docs
---
## Q
为什么聚簇深度偏高（重叠层数多）会预示着剪枝效果变差？

## A
剪枝依赖每个微分区在目标列上的取值范围与查询谓词是否相交来决定是否跳过整个分区。如果同一取值区间被很多个微分区同时覆盖（即重叠、聚簇深度高），那么只要谓词命中这个区间，所有覆盖它的微分区都无法被排除，必须全部保留扫描——即使每个分区里真正匹配的行很少。重叠层数越多，需要保留扫描的微分区就越多，剪枝的效果就越差。
