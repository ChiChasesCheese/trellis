---
id: polaris-catalog-linked-database
node: openplatform.polaris-catalog
type: qa
source: snowflake-docs
---
## Q
远程 Iceberg REST catalog 里有几百张表，而且不断新增。如何让 Snowflake 访问它们，而不必逐张执行 CREATE ICEBERG TABLE？

## A
创建一个目录链接数据库（catalog-linked database）：它通过 Iceberg REST 的 catalog integration（如 Snowflake Open Catalog）自动发现远程 catalog 中的命名空间和表并持续保持同步，Snowflake 可以直接读写这些表，同时保留与现有 Iceberg 生态的完全互操作。该功能只支持 Iceberg REST 类型的 catalog integration，不适用于基于对象存储元数据文件的集成。
