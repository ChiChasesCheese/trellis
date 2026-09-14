%% trellis:begin %%
# 最小/最大值剪枝（zone map）
*剪枝与查询优化*

在不打开文件的情况下，跳过那些最小/最大值范围无法满足谓词条件的整个微分区。

**Requires:** [[storage.micro-partition-metadata|微分区元数据]]

**Unlocks:** [[pruning.partition-elimination|分区消除（partition elimination）]]

## Readings
- [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]]

## Cards (5)
- [[pruning-zonemap-ideal-ratio]]
- [[pruning-zonemap-mechanism]]
- [[pruning-zonemap-partition-size]]
- [[pruning-zonemap-predicate-limits]]
- [[pruning-zonemap-vs-btree-index]]
%% trellis:end %%

## Notes
