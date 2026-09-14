---
id: task-serverless-privilege
node: pipelines.task-serverless-vs-warehouse
type: qa
source: snowflake-docs
---
## Q
一个角色能创建使用仓库的任务，却在创建无服务器任务时报权限不足。缺少什么权限？

## A
无服务器任务依赖 Snowflake 管理的计算资源，需要账户级的 `EXECUTE MANAGED TASK` 权限；而使用用户管理仓库的任务需要的是该仓库上的 `USAGE` 权限。两类任务还都需要数据库和模式的 USAGE 以及模式上的 CREATE TASK，任务所有者运行任务还需要账户级的 `EXECUTE TASK` 权限。
