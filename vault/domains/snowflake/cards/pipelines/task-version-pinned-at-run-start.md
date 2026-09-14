---
id: task-version-pinned-at-run-start
node: pipelines.task-scheduling-cron-and-dag
type: qa
source: snowflake-docs
---
## Q
任务正在运行时，所有者挂起了任务并修改了其 SQL。正在跑的这次运行用的是新代码还是旧代码？新代码何时生效？

## A
正在进行的运行继续使用它开始时的任务版本（旧代码）；挂起会取消所有尚未开始的后续调度，但不会中断已开始的运行。只有当任务再次被恢复（RESUME）或手动执行时，Snowflake 才设置包含修改的新版本。任务版本历史可以通过 Account Usage 中的 `TASK_VERSIONS` 视图查看。
