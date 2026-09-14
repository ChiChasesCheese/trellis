---
id: task-suspend-after-num-failures
node: pipelines.task-failure-handling
type: qa
source: snowflake-docs
---
## Q
一个任务因为上游表被删除而每次运行都失败，却一直按调度消耗信用点。怎样让 Snowflake 自动止损？该参数可以在哪些层级设置？

## A
设置 `SUSPEND_TASK_AFTER_NUM_FAILURES = <num>`（大于 0）：当任务连续失败或超时达到指定次数时，任务会被自动挂起，从而不再为跑不完的运行消耗信用点。该参数可以在 CREATE TASK / ALTER TASK 中设置，也可以在账户、数据库或模式级设置，作用于其中所有任务；在较低层级显式设置的值会覆盖较高层级的值。
