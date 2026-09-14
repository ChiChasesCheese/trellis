---
id: storage-compute-sep-vs-coupled-traditional
node: architecture.storage-compute-separation
type: qa
source: snowflake-docs
---
## Q
相比把存储和计算耦合在同一批节点上的传统数据仓库，Snowflake 把二者拆开之后，扩容方式有什么本质不同？

## A
在存储计算耦合的架构里，要扩大存储容量或提升计算能力，往往必须整体增加节点，即使真正的瓶颈只在其中一侧。Snowflake 把持久化存储和虚拟仓库计算拆成两套独立资源后，可以只针对遇到瓶颈的一侧单独扩容——例如只增大某个虚拟仓库应对计算压力，而不必因此重新分配或迁移存储层的数据。
