%% trellis:begin %%
# 列式压缩与编码
*存储引擎与微分区（micro-partition）*

按列选择编码方式并压缩，以及为何列式布局是让压缩和剪枝都变得廉价的根本原因。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/storage.micro-partition-format|微分区（micro-partition）格式]]

**Unlocks:** [[domains/snowflake/map/query.vectorized-columnar-execution|向量化列式执行]]

## Readings
- [[snowflak-micropartitions-clustering|微分区与数据聚簇的物理基础]]

## Cards (4)
1. [[compression-algorithm-per-column-per-partition]]
2. [[compression-columns-stored-independently]]
3. [[compression-no-user-encoding-ddl]]
4. [[compression-stored-size-smaller-than-50-500]]
%% trellis:end %%

## Notes
