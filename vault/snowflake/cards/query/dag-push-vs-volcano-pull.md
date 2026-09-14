---
id: dag-push-vs-volcano-pull
node: query.dag-execution-model
type: qa
tags: [grown]
---
## Q
Snowflake 执行引擎中的算子是 push-based（推模式）而不是经典 Volcano 风格的 pull-based（拉模式）。两者区别是什么？推模式带来什么好处？

## A
Volcano 拉模式下，上游算子反复调用下游的 `next()` 逐个拉取数据，控制流穿插在每次取数之中。推模式下，算子处理完一批数据后主动把结果推给它的下游算子。推模式把控制流逻辑移出紧密的处理循环，提升 CPU 缓存效率；更重要的是，一个算子可以把结果同时推给多个下游，因此执行计划可以是 DAG（有向无环图）而不只是树。
