---
id: multi-region-iceberg-external-storage
node: architecture.cloud-agnostic-multi-region
type: qa
source: snowflake-docs
---
## Q
如果数据必须留在自己管理的 S3、Google Cloud Storage 或 Azure Storage 桶里，Snowflake 用哪种表来查询它？数据的归属边界在哪里？

## A
用 Apache Iceberg tables（Iceberg 表）。它的数据文件和元数据文件都存放在用户管理的外部云存储位置，这块外部存储不属于 Snowflake；Snowflake 在其上提供与普通 Snowflake 表类似的性能和查询语义。与之相对，普通 Snowflake 表的数据会被重组为内部压缩列式格式，由 Snowflake 管理的云存储保存。
