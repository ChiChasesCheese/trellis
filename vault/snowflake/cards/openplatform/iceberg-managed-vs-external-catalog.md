---
id: iceberg-managed-vs-external-catalog
node: openplatform.iceberg-tables
type: qa
source: snowflake-docs
---
## Q
Snowflake 管理的 Iceberg 表（以 Snowflake 为 catalog）和使用外部 catalog 的 Iceberg 表，在平台功能支持和生命周期维护上有什么区别？

## A
以 Snowflake 为 catalog 的表获得完整平台支持：可读写、可设聚簇键（clustering key）、支持表复制，Snowflake 负责压实（compaction）等全部生命周期维护（可按需关闭压实）。使用外部 catalog（如 AWS Glue、远程 Iceberg REST catalog）的表只有有限的平台支持：Snowflake 通过 catalog integration 读取元数据，不承担任何生命周期管理，不支持聚簇，删除文件过多时需要用外部引擎（如 Spark 的 `rewrite_data_files`）自行维护。需要完整支持时可以把表转换为以 Snowflake 为 catalog。
