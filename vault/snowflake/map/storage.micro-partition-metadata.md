%% trellis:begin %%
# Micro-partition Metadata
*Storage Engine & Micro-partitions*

What the header of every micro-partition tracks (min/max per column, distinct counts, null counts) and where that metadata actually lives.

**Requires:** [[storage.micro-partition-format|Micro-partition Format]]

**Unlocks:** [[storage.clustering-keys|Clustering Keys]], [[metadata.optimizer-statistics|Optimizer Statistics]], [[pruning.min-max-zone-maps|Min/Max Pruning (Zone Maps)]], [[cache.metadata-cache-pruning-stats|Metadata Cache for Pruning]]
%% trellis:end %%

## Notes
