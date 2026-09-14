---
id: task-owner-role-dropped-paused
node: pipelines.task-failure-handling
type: qa
source: snowflake-docs
---
## Q
管理员删除了一个角色，而这个角色是若干任务的所有者。这些任务之后还会按调度运行吗？正在运行的那次呢？

## A
被删除角色所拥有的任务，所有权会转移给执行删除操作的角色；所有权转移时任务会被自动暂停，在新所有者恢复任务之前不会调度新的运行。如果删除角色时任务正在运行，这次运行会在已删除的角色下继续处理完。另外，撤销所有者角色的 `EXECUTE TASK` 权限，会阻止该角色下所有后续任务运行的启动。
