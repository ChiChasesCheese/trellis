---
id: natural-vs-explicit-manual-sort-alternative
node: storage.natural-vs-explicit-clustering
type: qa
source: snowflake-docs
---
## Q
不用聚簇键（clustering key），自己把大表按关键列排序后重新插入，也能恢复聚簇，为什么 Snowflake 仍推荐显式聚簇键？

## A
手工排序再插入是一次性的，而且对大表来说既繁琐又昂贵，随后 DML 又会让聚簇重新退化，需要反复做。定义聚簇键后，Snowflake 会自动持续维护聚簇，只在表能受益时才重写微分区（micro-partition），无需人工监控或调度。代价是这种维护消耗 credit（信用点），所以只值得用在查询收益明显的表上。
