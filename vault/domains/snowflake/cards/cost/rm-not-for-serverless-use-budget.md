---
id: rm-not-for-serverless-use-budget
node: cost.resource-monitors-and-budgets
type: qa
source: snowflake-docs
---
## Q
账户级资源监控器（account monitor）设置了每月 5000 credit 并配置了挂起，Snowpipe、自动重新聚簇和物化视图维护的费用会被它拦住吗？应该用什么来控制这部分支出？

## A
不会。资源监控器只作用于虚拟仓库（及支撑仓库的云服务），账户级监控器也不控制 Snowflake 为无服务器功能（如 Snowpipe、自动重新聚簇、物化视图）提供的计算资源，也无法跟踪 AI 服务的支出。要监控这些功能的信用点消耗，应使用预算（budget）。另外，仓库级监控器能统计但不能挂起云服务用量：仓库被挂起后，针对它提交的查询仍可能产生云服务费用。
