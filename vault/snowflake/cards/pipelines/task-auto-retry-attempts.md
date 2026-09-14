---
id: task-auto-retry-attempts
node: pipelines.task-failure-handling
type: qa
source: snowflake-docs
---
## Q
任务偶尔因瞬时错误失败，希望 Snowflake 自动重试。默认会重试吗？如何开启？开启后错误通知有什么变化？

## A
默认不重试，自动重试是关闭的。把 `TASK_AUTO_RETRY_ATTEMPTS` 设为大于 0 的值即可开启：任务以 FAILED 状态结束时会被自动重试。在账户、数据库或模式级设置该参数时，变化在其中任务的下一次调度运行时生效。配置了错误通知的任务，会为每一次失败的重试都发送一条通知。
