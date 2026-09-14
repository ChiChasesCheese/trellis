---
id: serverless-why-model
node: cost.serverless-feature-billing
type: qa
source: snowflake-docs
---
## Q
Snowpipe、搜索优化（Search Optimization）这类功能为什么用 Snowflake 管理的无服务器（serverless）计算，而不是跑在用户自己的虚拟仓库上？这对计费有什么好处？

## A
这类功能通常需要持续运行或做后台维护，负载时大时小。用户管理的仓库只要在运行就计费，不论是否在干活，很容易要么过度使用、要么空转。无服务器计算由 Snowflake 按每个工作负载自动调整规模和伸缩，只按实际使用资源的时间计费，避免为空闲容量付费，也免去用户为后台任务专门规划仓库。
