---
id: auto-recluster-not-under-resource-monitor
node: storage.automatic-reclustering
type: qa
source: snowflake-docs
---
## Q
一个团队用 resource monitor（资源监控器）给所有虚拟仓库设了信用点上限，为什么账单里自动聚簇（Automatic Clustering）的花费仍可能失控？怎么控制？

## A
resource monitor 只能控制用户虚拟仓库的 credit 用量，无法约束 Snowflake 提供的内部仓库，包括执行自动聚簇的 AUTOMATIC_CLUSTERING 仓库。控制方法是：先只在一两张表上启用并观察 credit 基线；用 `AUTOMATIC_CLUSTERING_HISTORY` 视图按天、按表监控花费；需要时暂停或删除聚簇键。
