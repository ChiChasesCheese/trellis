---
id: cs-low-warehouse-high-services
node: cost.cloud-services-free-tier
type: qa
source: snowflake-docs
---
## Q
什么样的工作负载最容易让云服务（Cloud Services）费用真正出现在账单上？为什么？

## A
云服务开销高而仓库用量低的负载，因为免费额度与仓库用量成比例。典型例子：大量几乎不耗仓库算力、但每条都要编译和访问元数据的语句，如高频的小查询、频繁的 DDL、大量 SHOW/DESCRIBE 等元数据命令、非常复杂需要长时间编译的查询。这些语句主要消耗云服务层资源，仓库用量却很少，于是云服务消耗容易超过当天仓库用量的 10%。
