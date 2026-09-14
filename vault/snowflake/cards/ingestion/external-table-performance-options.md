---
id: external-table-performance-options
node: ingestion.external-tables-over-lake
type: qa
source: snowflake-docs
---
## Q
外部表上的高频复杂查询明显比原生表慢。有哪些提速手段？

## A
1) 按日期、国家等逻辑路径对外部表做分区，查询只扫描相关分区；2) 在外部表上建物化视图（materialized view），高频或复杂查询可能显著加快（需保持元数据刷新，物化视图才能反映最新文件）；3) 控制文件大小以提升并行扫描度，Parquet 文件建议 256–512 MB，行组 16–256 MB；4) 对 Parquet 数据，若追求最佳性能，可以考虑改用 Apache Iceberg 表。
