---
id: task-runs-as-system-service
node: pipelines.task-scheduling-cron-and-dag
type: qa
source: snowflake-docs
---
## Q
创建任务的员工离职、账号被删除后，他创建的定时任务会停止吗？为什么？

## A
不会。默认情况下，任务由一个与具体用户解耦的系统服务运行，使用任务所有者角色的权限，因此用户被删除、被锁定或被移除角色都不会中断任务。只有配置了 `EXECUTE AS USER` 的任务才以特定用户身份运行，那种情况下人员变动可能中断任务，所以生产环境建议使用专门的服务用户。
