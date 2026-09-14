---
id: compiler-pruning-cost-on-huge-tables
node: metadata.query-compiler-pipeline
type: qa
tags: [grown]
---
## Q
一张拥有海量微分区（micro-partition）的大表，或层层嵌套的复杂视图，为什么可能让 Snowflake 查询在还没开始执行时就花掉明显时间？这部分工作怎么计费？

## A
编译阶段不仅要解析和优化 SQL，还要依据元数据为每张表确定需要扫描的微分区集合（剪枝），并展开视图定义；分区越多、视图越复杂，云服务（Cloud Services）层要读取和处理的元数据就越多，编译时间随之增长。这部分计算消耗的是云服务 credit，而不是仓库 credit；云服务用量只有超出当日虚拟仓库用量 10% 的部分才会计费。
