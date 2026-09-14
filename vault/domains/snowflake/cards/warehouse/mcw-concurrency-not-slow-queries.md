---
id: mcw-concurrency-not-slow-queries
node: warehouse.multi-cluster-scaling-policy
type: qa
source: snowflake-docs
---
## Q
什么问题适合用多集群仓库（multi-cluster warehouse）解决，什么问题不适合？首次配置集群数时建议怎样起步？

## A
适合：大量并发用户/查询导致的排队，以及并发量随时间波动的负载——它让更多用户连到同一规格的仓库，Auto-scale 模式下无需手工调规格或启停额外仓库。不适合：单条慢查询或数据加载慢，这类问题调大仓库规格更有效。起步建议用 Auto-scale 模式、从小开始（如最小 1、最大 2 或 3），观察负载波动后再逐步调整上下限。
