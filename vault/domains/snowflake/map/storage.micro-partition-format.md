%% trellis:begin %%
# 微分区（micro-partition）格式
*存储引擎与微分区（micro-partition）*

每张表在物理上都以 50-500MB 的不可变列式文件单元存储，以及为何不可变性是下游一切功能的前提条件。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/architecture.storage-compute-separation|存储与计算分离（storage/compute separation）]]

**Unlocks:** [[domains/snowflake/map/storage.micro-partition-metadata|微分区元数据]], [[domains/snowflake/map/storage.columnar-compression-encoding|列式压缩与编码]], [[domains/snowflake/map/storage.table-types|表类型]], [[domains/snowflake/map/txn.mvcc-immutable-partitions|基于不可变微分区的 MVCC]], [[domains/snowflake/map/semistructured.variant-type-storage|VARIANT 类型与存储]]

## Readings
- [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]]

## Cards (5)
1. [[micro-partition-columnar-inside]]
2. [[micro-partition-drop-column-no-rewrite]]
3. [[micro-partition-overlap-prevents-skew]]
4. [[micro-partition-size-50-500mb-uncompressed]]
5. [[micro-partition-vs-static-partitioning]]
%% trellis:end %%

## Notes
