%% trellis:begin %%
# 微分区元数据
*存储引擎与微分区（micro-partition）*

每个微分区的头部记录了什么（每列的最小值/最大值、去重计数、空值计数），以及这些元数据实际存放在哪里。

**Requires:** [[storage.micro-partition-format|微分区（micro-partition）格式]]

**Unlocks:** [[storage.clustering-keys|聚簇键（clustering key）]], [[metadata.optimizer-statistics|优化器统计信息]], [[pruning.min-max-zone-maps|最小/最大值剪枝（zone map）]], [[cache.metadata-cache-pruning-stats|用于剪枝的元数据缓存]]

## Readings
- [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]]

## Cards (5)
- [[mp-metadata-collected-at-load]]
- [[mp-metadata-dml-maintenance]]
- [[mp-metadata-per-partition-contents]]
- [[mp-metadata-semistructured-columns]]
- [[mp-metadata-table-level-clustering-stats]]
%% trellis:end %%

## Notes
