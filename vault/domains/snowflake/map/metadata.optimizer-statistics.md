%% trellis:begin %%
# 优化器统计信息
*元数据与云服务*

优化器从微分区元数据中提取哪些统计信息（基数、去重值）来选择执行计划，且无需扫描数据本身。

**Requires:** [[storage.micro-partition-metadata|微分区元数据]]

## Readings
- [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]]

## Cards (4)
- [[optimizer-stats-contents]]
- [[optimizer-stats-never-stale-after-dml]]
- [[optimizer-stats-no-analyze-command]]
- [[optimizer-stats-plan-without-reading-data]]
%% trellis:end %%

## Notes
