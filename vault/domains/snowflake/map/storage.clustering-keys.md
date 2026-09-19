%% trellis:begin %%
# 聚簇键（clustering key）
*存储引擎与微分区（micro-partition）*

选择聚簇键以让相关的微分区聚集在一起，以及真正能从中受益的访问模式。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/storage.micro-partition-metadata|微分区元数据]]

**Unlocks:** [[domains/snowflake/map/storage.automatic-reclustering|自动重新聚簇（automatic reclustering）]], [[domains/snowflake/map/storage.natural-vs-explicit-clustering|自然聚簇与显式聚簇]], [[domains/snowflake/map/pruning.clustering-depth-metric|聚簇深度（clustering depth）]]

## Readings
- [[snowflak-clustering-keys-strategy|聚簇键的选择与何时需要它]]
- [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]]

## Cards (6)
1. [[clustering-key-cardinality-sweet-spot]]
2. [[clustering-key-column-order-low-to-high]]
3. [[clustering-key-ctas-clone-hybrid]]
4. [[clustering-key-filter-join-over-groupby]]
5. [[clustering-key-text-prefix-bytes]]
6. [[clustering-key-when-worth-it]]
%% trellis:end %%

## Notes
