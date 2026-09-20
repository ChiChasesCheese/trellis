%% trellis:begin %%
# 微分区元数据
*存储引擎与微分区（micro-partition）*

每个微分区的头部记录了什么（每列的最小值/最大值、去重计数、空值计数），以及这些元数据实际存放在哪里。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/storage.micro-partition-format|微分区（micro-partition）格式]]

**Unlocks:** [[domains/snowflake/map/storage.clustering-keys|聚簇键（clustering key）]], [[domains/snowflake/map/metadata.optimizer-statistics|优化器统计信息]], [[domains/snowflake/map/pruning.min-max-zone-maps|最小/最大值剪枝（zone map）]], [[domains/snowflake/map/cache.metadata-cache-pruning-stats|用于剪枝的元数据缓存]]

## Readings
- [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]]

## Cards (5)
1. [[mp-metadata-collected-at-load]]
2. [[mp-metadata-dml-maintenance]]
3. [[mp-metadata-per-partition-contents]]
4. [[mp-metadata-semistructured-columns]]
5. [[mp-metadata-table-level-clustering-stats]]
%% trellis:end %%

## Notes
