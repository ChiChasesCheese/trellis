---
id: task-timeout-parameters
node: pipelines.task-failure-handling
type: qa
source: snowflake-docs
---
## Q
同时设置了 `STATEMENT_TIMEOUT_IN_SECONDS` 和 `USER_TASK_TIMEOUT_MS` 时，任务的超时以哪个为准？排队超时参数又如何？

## A
任务运行超过调度时间或目标完成间隔时，默认会继续运行，直到完成、超时或失败。两者都设置时，超时取两个参数中较小的非零值。若同时设置了 `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS` 和 `USER_TASK_TIMEOUT_MS`，则以 `USER_TASK_TIMEOUT_MS` 为准。超时同样计入连续失败次数，可能触发自动挂起。
