---
id: stream-stale-definition-recreate
node: pipelines.stream-staleness-and-retention-extension
type: qa
source: snowflake-docs
---
## Q
什么情况下一个流（Stream）会变得陈旧（stale）？陈旧之后还能恢复读取未消费的变更吗？

## A
当流的偏移量落到源表（或视图底层表）的数据保留期（data retention period）之外时，流就会陈旧，因为计算变更所依赖的历史版本已不可访问。陈旧状态下，源表的历史数据和所有未消费的变更记录都无法再访问；要继续追踪新变更，只能用 `CREATE STREAM` 重新创建流，中间丢失的变更需要另行补数。
