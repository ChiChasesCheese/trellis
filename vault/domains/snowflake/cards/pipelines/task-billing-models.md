---
id: task-billing-models
node: pipelines.task-serverless-vs-warehouse
type: qa
source: snowflake-docs
---
## Q
一个每 30 秒运行、每次只跑 5 秒的轻量任务，放在用户管理的仓库上和作为无服务器任务运行，计费方式有什么区别？

## A
用户管理仓库按仓库规格和运行时间计费，并且仓库每次恢复运行都至少收取 60 秒；若仓库在两次运行之间自动挂起，每次恢复都会触发这 60 秒最低计费，不挂起则空闲时间也在计费。无服务器任务按实际使用的计算资源（含云服务使用）以计算小时（compute-hours）计费，没有每次恢复的最低时长，因此更适合这种短小而频繁的任务。
