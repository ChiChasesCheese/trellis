---
id: task-graph-root-and-children
node: pipelines.task-scheduling-cron-and-dag
type: qa
source: snowflake-docs
---
## Q
什么是任务图（task graph）？其中的任务如何声明先后依赖？调度定义在哪个任务上？

## A
任务图是把多个任务组织成有向无环图（DAG）的工作流，任务之间可以串行也可以并行。只有根任务（root task）定义 `SCHEDULE`（或触发条件）；子任务不定义调度，而是用 `AFTER <前驱任务>` 声明依赖，在所有前驱任务成功完成后运行。任务图还可以带逻辑，实现动态的并行或串行执行。
