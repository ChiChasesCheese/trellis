---
id: pruning-elimination-hour-example
node: pruning.partition-elimination
type: qa
source: snowflake-docs
---
## Q
一张存有一年历史数据、包含 date 和 hour 列的大表，在数据均匀分布的理想情况下，一条只查询某一个小时数据的查询，分区消除后理想应该只需要扫描全表微分区的多大比例？

## A
理想情况下只需要扫描约 1/8760（一年 365 天 × 24 小时 = 8760 小时）的微分区，因为分区消除会先排除掉不包含目标小时数据的绝大多数微分区；这也是为什么在时间序列数据上，即使切片粒度细到一小时甚至更小，也能做到亚秒级的查询响应。
