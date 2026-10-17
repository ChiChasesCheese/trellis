---
id: amz-dag-runner-objects-and-their-jobs
node: amazon.amz-dag-runner
type: qa
step: 2
tags: [grown]
---
## Q
在 Amazon DAG 执行器设计里，需要哪几个对象？各自的一个职责是什么？

## A
Graph：不可变依赖图，边去重，只管排序、找环、求后代，不知道执行。CycleError：带着环本身的异常。Step：冻结数据类（名字、函数、依赖名）。Workflow：登记步骤并执行，运行前建图检查环。RunReport：并行结局，每个步骤恰好在成功、失败、跳过三个桶之一。拆分依据：图的算法与执行分开，第一关函数能单独使用。
