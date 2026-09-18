%% trellis:begin %%
# 分区消除（partition elimination）
*剪枝与查询优化*

剪枝决策如何仅凭元数据在编译期做出，从而把一次全表扫描变成对存活微分区集合的扫描。

**Requires:** [[domains/snowflake/map/pruning.min-max-zone-maps|最小/最大值剪枝（zone map）]]

**Unlocks:** [[domains/snowflake/map/pruning.search-optimization-service|搜索优化服务（Search Optimization Service）]], [[domains/snowflake/map/pruning.materialized-views-maintenance|物化视图（materialized view）]]

## Readings
- [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]]
- [[snowflak-query-profile-history|查询画像(Query Profile)与查询历史的定位方法]]

## Cards (5)
- [[pruning-elimination-hour-example]]
- [[pruning-elimination-metadata-only-dml]]
- [[pruning-elimination-not-index-probe]]
- [[pruning-elimination-two-stage]]
- [[pruning-elimination-vs-full-scan]]
%% trellis:end %%

## Notes
