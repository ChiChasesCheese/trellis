%% trellis:begin %%
# 优化器统计信息
*元数据与云服务*

优化器从微分区元数据中提取哪些统计信息（基数、去重值）来选择执行计划，且无需扫描数据本身。

**Requires:** [[domains/snowflake/map/storage.micro-partition-metadata|微分区元数据]]

## Readings
- [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]]

## Cards (4)
1. [[optimizer-stats-contents]]
2. [[optimizer-stats-never-stale-after-dml]]
3. [[optimizer-stats-no-analyze-command]]
4. [[optimizer-stats-plan-without-reading-data]]
%% trellis:end %%

## Notes
