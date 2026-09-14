---
id: task-created-suspended
node: pipelines.task-scheduling-cron-and-dag
type: qa
source: snowflake-docs
---
## Q
`CREATE TASK` 成功并定义了 `SCHEDULE` 之后，任务（Task）却从来没有运行过。为什么？如何测试和启用？

## A
任务创建后默认处于挂起（suspended）状态，不会按调度运行。先用 `EXECUTE TASK` 手动触发一次进行测试，确认无误后执行 `ALTER TASK … RESUME`，任务才会按调度持续运行或持续检测事件。恢复时，Snowflake 还会校验任务所有者角色是否具备运行所需的权限（如账户级的 EXECUTE TASK）。
