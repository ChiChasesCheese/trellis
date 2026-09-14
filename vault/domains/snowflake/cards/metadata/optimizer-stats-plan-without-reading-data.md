---
id: optimizer-stats-plan-without-reading-data
node: metadata.optimizer-statistics
type: qa
source: snowflake-docs
---
## Q
一张一年期、按小时均匀分布的大表，查询只取某一个小时的数据。Snowflake 在不读任何数据的前提下，能从统计信息中得出多少数据需要扫描？

## A
依据每个微分区（micro-partition）记录的列取值范围，优化器可以判断哪些分区可能包含目标小时。在数据均匀分布时，理想情况下只需扫描表中约 1/8760 的微分区，并且在这些分区里只读取查询涉及的列。这一判断完全基于元数据，在分配计算资源读取数据之前就能做出，因此即使表有数百万个微分区，计划阶段也不需要触碰数据本身。
