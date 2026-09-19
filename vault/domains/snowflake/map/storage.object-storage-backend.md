%% trellis:begin %%
# 对象存储后端
*存储引擎与微分区（micro-partition）*

为何每个微分区都是云对象存储（S3/Blob/GCS）中的一个 blob 而不是本地磁盘文件，以及这样做的收益与代价。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/architecture.storage-compute-separation|存储与计算分离（storage/compute separation）]]

**Unlocks:** [[domains/snowflake/map/ingestion.external-tables-over-lake|数据湖之上的外部表]], [[domains/snowflake/map/openplatform.iceberg-tables|Iceberg 表]]

## Readings
- [[snowflak-key-concepts-architecture|Snowflake 关键概念与整体架构]]

## Cards (4)
1. [[object-storage-central-repo-plus-local-cache]]
2. [[object-storage-hybrid-table-contrast]]
3. [[object-storage-snowflake-managed-layout]]
4. [[object-storage-snowflake-vs-iceberg-ownership]]
%% trellis:end %%

## Notes
