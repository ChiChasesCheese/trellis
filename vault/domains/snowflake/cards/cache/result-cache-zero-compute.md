---
id: result-cache-zero-compute
node: cache.result-cache
type: qa
source: snowflake-docs
---
## Q
Snowflake 的持久化结果缓存（persisted query result cache）命中时，查询是如何返回结果的？这与重新运行一次相同规模的查询相比，成本上有什么本质区别？

## A
命中结果缓存时，Snowflake 直接把此前已经计算好、存放在云服务（Cloud Services）层的结果返回给客户端，完全跳过对微分区数据的扫描与计算，因此不消耗任何计算信用点（credit）——即使发起查询的虚拟仓库当前处于挂起（suspended）状态也能命中，因为结果缓存独立于任何仓库存在。
