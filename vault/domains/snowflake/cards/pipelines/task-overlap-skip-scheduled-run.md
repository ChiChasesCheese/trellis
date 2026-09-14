---
id: task-overlap-skip-scheduled-run
node: pipelines.task-scheduling-cron-and-dag
type: qa
source: snowflake-docs
---
## Q
一个每 5 分钟调度一次的任务，某次运行耗时 12 分钟。期间到点的调度会排队叠加执行吗？

## A
不会。Snowflake 保证一个带调度的任务同一时刻只运行一个实例：如果到了下一个调度时间点，上一次运行仍未结束，这次调度会被直接跳过，而不是排队或并发执行。因此运行时间超过调度间隔会导致实际执行频率下降。
