---
id: reader-compute-billed-to-provider
node: sharing.reader-accounts
type: qa
source: snowflake-docs
---
## Q
只读账户（reader account）里的用户查询共享数据消耗的计算费用由谁承担？这给提供方带来什么成本风险，怎么控制？

## A
只读账户由提供方创建和管理，其中虚拟仓库（virtual warehouse）的计算消耗计入提供方账户的账单，而不是由读者方付费。风险是读者方大量或低效查询会直接推高提供方的成本。提供方应为只读账户创建尺寸受限的仓库、设置自动挂起，并用资源监控器（resource monitor）给这些仓库设信用点上限。
