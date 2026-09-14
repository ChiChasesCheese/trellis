---
id: dag-shared-intermediate-results
node: query.dag-execution-model
type: qa
tags: [grown]
---
## Q
为什么说 Snowflake 的执行计划是 DAG（有向无环图）而不只是树，这对一个在查询里被引用两次的 CTE（公共表表达式）有什么意义？

## A
树形计划中每个算子只有一个父节点，同一个中间结果被两处使用时往往要计算两遍。DAG 允许一个算子有多个下游消费者：CTE 的结果可以计算一次，再同时推送给引用它的两个分支，实现中间结果的共享与流水线化（pipelining），省去重复计算。
