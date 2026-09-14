---
id: dag-failure-whole-query-retry
node: query.dag-execution-model
type: qa
tags: [grown]
---
## Q
一条查询的 DAG 分布在虚拟仓库（virtual warehouse）多个工作节点上执行，其中一个节点中途故障，Snowflake 如何处理？这种设计为什么可行？

## A
Snowflake 不做算子级或节点级的部分重试，而是让整条查询重新执行（对用户透明地重试）。这可行是因为工作节点是无状态的：输入是不可变的微分区文件，中间结果只在本次查询内有意义，重跑能得到同样结果，也不会破坏已提交的数据。代价是长查询在故障时要从头再来。
