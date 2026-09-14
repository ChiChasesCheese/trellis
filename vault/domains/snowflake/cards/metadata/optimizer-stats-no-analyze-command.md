---
id: optimizer-stats-no-analyze-command
node: metadata.optimizer-statistics
type: qa
source: snowflake-docs
---
## Q
在传统数据库里要定期跑 `ANALYZE` 收集优化器统计信息（optimizer statistics），为什么在 Snowflake 普通表上不需要这一步？

## A
Snowflake 全权管理表数据的元数据与统计信息：数据插入/加载时，每创建一个微分区（micro-partition），Snowflake 就同时收集并记录该分区的元数据，包括每列取值范围、不同值数量等用于优化的属性。统计信息是写入路径的副产品，而不是事后单独扫描表得到的，所以用户不需要、也没有手段去触发统计收集。
