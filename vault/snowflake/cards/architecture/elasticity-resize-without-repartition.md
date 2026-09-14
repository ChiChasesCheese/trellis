---
id: elasticity-resize-without-repartition
node: architecture.elasticity-multitenancy
type: qa
tags: [grown]
---
## Q
传统 shared-nothing（无共享）MPP 数仓扩容往往要重新分布数据、耗时数小时，为什么 Snowflake 的虚拟仓库（virtual warehouse）能在秒级增减节点？代价是什么？

## A
因为数据的持久副本放在共享的云对象存储里，计算节点（worker node）不“拥有”任何数据，只在本地缓存近期读过的文件。加减节点不需要搬迁或重新分区数据，只是改变参与执行的节点集合，新节点直接从对象存储读取所需文件。代价是新节点的本地缓存是冷的，扩容后的最初几条查询要更多地从远程存储读取，速度会慢一些。
