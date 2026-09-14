---
id: task-queuing-shared-warehouse
node: pipelines.task-serverless-vs-warehouse
type: qa
source: snowflake-docs
---
## Q
一个用户管理仓库上的任务「总耗时」越来越长，但 SQL 本身执行很快。应如何定位？与无服务器任务相比原因是什么？

## A
任务总时长 = 排队时间 + 执行时间。用 `TASK_HISTORY` 视图对比 `SCHEDULED_TIME` 与 `QUERY_START_TIME` 得到排队时间，对比 `QUERY_START_TIME` 与 `COMPLETED_TIME` 得到执行时间。任务调度在共享或繁忙的仓库上时，常常要长时间等待计算资源；无服务器任务则由 Snowflake 自动扩展资源，力求在目标完成间隔内（含排队）完成。解决方法是给任务分配专用仓库，或改为无服务器任务。
