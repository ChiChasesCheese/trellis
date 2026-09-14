---
id: storage-compute-sep-independent-scaling
node: architecture.storage-compute-separation
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 里，存储与计算分离具体指什么，这为数据工程带来了什么好处？

## A
持久化数据存放在云存储中，而实际执行 SQL 的计算资源是一个个独立的虚拟仓库（virtual warehouse）；两者是两套完全独立的资源，不绑定在同一批物理节点上。这样数据工程师不必再把存储容量规划和计算资源规划耦合在一起处理，基础设施管理和性能调优被大幅简化，可以专注于设计数据摄取、转换与交付的流水线本身。
