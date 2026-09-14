---
id: compile-plan-carries-file-list
node: query.compilation-pipeline
type: qa
tags: [grown]
---
## Q
编译完成后交给虚拟仓库（virtual warehouse）的物理计划里包含了什么？为什么工作节点执行时不需要自己去查元数据存储？

## A
物理计划包含由算子组成的执行步骤，以及每个表扫描在剪枝之后需要读取的微分区（micro-partition）文件列表。剪枝和对象解析都已在云服务（Cloud Services）层依据元数据完成，工作节点只需按计划从对象存储读取指定文件并执行算子，不需要直接访问元数据存储。这让计算节点保持无状态、易于增减，也把元数据访问集中在云服务层。
