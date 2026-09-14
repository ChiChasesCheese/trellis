---
id: multi-cluster-shared-data-hybrid-benefit
node: architecture.multi-cluster-shared-data
type: qa
source: snowflake-docs
---
## Q
为什么说 Snowflake 的多集群共享数据模型同时拿到了共享磁盘架构和无共享架构各自的优点？

## A
它从共享磁盘架构那里继承了数据管理的简单性——只有一份集中存放的数据，不需要手工分片或维护多份副本；又从无共享架构那里继承了横向扩展（scale-out）的性能优势——通过大规模并行处理（MPP），把计算任务分发到多个各自缓存一部分数据的节点上并行执行，而不是让所有节点挤在一条磁盘 I/O 通路上。
