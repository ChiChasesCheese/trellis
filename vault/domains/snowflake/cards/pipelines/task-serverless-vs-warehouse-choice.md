---
id: task-serverless-vs-warehouse-choice
node: pipelines.task-serverless-vs-warehouse
type: qa
source: snowflake-docs
---
## Q
什么情况下应选择无服务器任务，什么情况下应选择用户管理仓库的任务？

## A
无服务器任务适合：专用仓库利用率低（任务少、运行快）、运行时长相对稳定，以及非常看重按时完成的场景，因为运行超出调度间隔时 Snowflake 会自动加大资源。用户管理仓库的任务适合：仓库已被多个并发任务充分利用、计算负载不可预测，或需要超过 XXLARGE 的仓库；此时开启自动挂起/恢复的多集群仓库有助于控制信用点消耗。
