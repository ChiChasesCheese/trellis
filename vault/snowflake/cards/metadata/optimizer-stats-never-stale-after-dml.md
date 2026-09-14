---
id: optimizer-stats-never-stale-after-dml
node: metadata.optimizer-statistics
type: qa
source: snowflake-docs
---
## Q
传统数据库在大批量写入后常因统计信息过期（stale statistics）选出糟糕的执行计划。Snowflake 的统计信息为什么不太会出现这个问题？

## A
Snowflake 的统计信息挂在每个微分区（micro-partition）上，并在数据写入、生成新微分区的同一过程中记录下来。表数据一旦变化，新数据所在的微分区从诞生起就带着准确的元数据，不存在“数据已写入但统计还没更新”的时间窗口，也就无需等待一次单独的统计刷新任务。
