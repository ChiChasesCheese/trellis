---
id: natural-vs-explicit-indicators
node: storage.natural-vs-explicit-clustering
type: qa
source: snowflake-docs
---
## Q
判断一张 Snowflake 大表该从自然聚簇改为定义显式聚簇键（clustering key），应该看哪两个信号？为什么不能只看其中的指标？

## A
两个信号：① 该表上的查询比预期慢，或随时间明显变慢；② 表在常用过滤列上的聚簇深度（clustering depth，重叠微分区的平均深度，越小越好）很大。不能只看深度，因为深度并不是衡量聚簇好坏的绝对精确指标，查询性能才是最终标准——查询够快就说明聚簇已经足够。可用 `SYSTEM$CLUSTERING_INFORMATION` 对任意列计算深度，即使表没有聚簇键；动手前应先用一组代表性查询建立性能基线。
