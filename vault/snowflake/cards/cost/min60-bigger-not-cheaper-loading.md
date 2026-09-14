---
id: min60-bigger-not-cheaper-loading
node: cost.warehouse-billing-60s-minimum
type: qa
source: snowflake-docs
---
## Q
按秒计费下常见的想法是“仓库调大一倍、查询快一倍，总花费不变”。为什么这对数据加载和小查询往往不成立？

## A
只有当查询能充分利用翻倍的资源、耗时真正减半时，翻倍的每秒费率才会被抵消。数据加载性能主要取决于文件数量和单个文件大小，而非仓库尺寸；除非并发加载成百上千个文件，Small/Medium/Large 通常就够了，更大的仓库只多耗信用点而不提速。小而简单的查询也不会因仓库变大而变快。此时加大仓库是纯粹多花钱，而且每次启动的 60 秒最低计费也按更高的费率收取。
