---
id: amz-dag-runner-followup-results-flow-between-steps
node: amazon.amz-dag-runner
type: qa
step: 6
tags: [grown]
---
## Q
在 Amazon DAG 执行器里，面试官追问「每个节点是一个函数，上游的结果要传给下游」（Step Function 式），在哪里改？什么不动？

## A
新增 Step（名字、函数、依赖名）和 Workflow.run：按 Graph.order() 执行，每个函数入参是 {依赖名: 结果} 字典，只含它声明的依赖。Graph、CycleError、install_order 一个字不改。例：load→10，double 收到 {"load":10} 返回 20。失败时抛 StepError 指出步骤名，后继不再运行。
