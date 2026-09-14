---
id: cloud-services-query-optimization-before-warehouse
node: architecture.cloud-services-layer
type: qa
source: snowflake-docs
---
## Q
为什么说 Snowflake 的查询解析与优化（query parsing and optimization）发生在虚拟仓库（virtual warehouse）开始执行之前，而且不在仓库里做？

## A
查询解析与优化是云服务（Cloud Services）层管理的服务之一。云服务层掌握元数据（metadata），可以在不读取表数据的情况下决定执行计划，然后才把计划派发给虚拟仓库执行。因此执行计划的制定依赖的是集中管理的元数据，而不是某个仓库本地的状态。
