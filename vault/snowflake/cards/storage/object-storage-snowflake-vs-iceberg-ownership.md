---
id: object-storage-snowflake-vs-iceberg-ownership
node: storage.object-storage-backend
type: qa
source: snowflake-docs
---
## Q
普通 Snowflake 表与 Apache Iceberg table（Iceberg 表）在“数据文件放在谁的存储里”上有什么区别？什么场景该选 Iceberg 表？

## A
普通 Snowflake 表的数据由 Snowflake 转换为内部格式后存放在 Snowflake 管理的云存储中；Iceberg 表的数据文件和元数据文件都放在用户自己管理的外部云存储位置（如 Amazon S3、Google Cloud Storage、Azure Storage），这块存储不属于 Snowflake。当已有数据湖或湖仓（lakehouse）、不能或不想把数据存进 Snowflake 时选 Iceberg 表，同时仍能获得接近普通表的性能和查询语义。
