---
id: three-layer-warehouse-independence
node: architecture.three-layer-model
type: qa
source: snowflake-docs
---
## Q
为什么在 Snowflake 中，一个虚拟仓库（virtual warehouse）跑重查询不会拖慢另一个虚拟仓库？

## A
因为每个虚拟仓库都是一个独立的计算集群，不与其他虚拟仓库共享任何计算资源（CPU、内存、本地磁盘缓存）。它们只是同时挂载在同一份共享的持久化数据之上；只要不共用计算资源，一个仓库的负载峰值就不会挤占另一个仓库的算力。
