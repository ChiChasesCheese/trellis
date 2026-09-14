---
id: pruning-depth-constant-state
node: pruning.clustering-depth-metric
type: qa
source: snowflake-docs
---
## Q
在聚簇深度的语境里，什么叫一张表的微分区达到了“constant state（恒定状态）”？处于恒定状态是否意味着这张表的所有微分区都不再有重叠？

## A
当一张表在指定列上，所有微分区之间的取值范围都不再互相重叠时，就称这些微分区达到了恒定状态（constant state），意味着继续做聚簇（clustering）已经无法再降低重叠、无法进一步改善剪枝效果了。但恒定状态是一个理论上的极限：对于包含大量微分区的真实大表，让所有微分区两两都不重叠既不现实也没有必要，只要重叠程度足够低、查询性能达标即可。
