---
id: task-serverless-how-sized
node: pipelines.task-serverless-vs-warehouse
type: qa
source: snowflake-docs
---
## Q
无服务器任务（serverless task）没有指定仓库，Snowflake 如何决定它用多大的计算资源？可以设定哪些边界？

## A
创建任务时不写 `WAREHOUSE` 参数即为无服务器任务。Snowflake 基于对同一任务最近几次运行的动态分析，预测并分配在调度时间内完成所需的资源，每次运行后复盘性能再调整后续运行。可以用 `SERVERLESS_TASK_MIN_STATEMENT_SIZE`（默认 XSMALL，保证性能下限）和 `SERVERLESS_TASK_MAX_STATEMENT_SIZE`（默认 XXLARGE，防止意外成本）限定范围；无服务器任务的上限相当于 XXLARGE 仓库。
