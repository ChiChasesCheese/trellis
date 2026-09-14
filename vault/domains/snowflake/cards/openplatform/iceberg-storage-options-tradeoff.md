---
id: iceberg-storage-options-tradeoff
node: openplatform.iceberg-tables
type: qa
source: snowflake-docs
---
## Q
创建 Iceberg 表时，选 Snowflake 存储（`EXTERNAL_VOLUME = SNOWFLAKE_MANAGED`）与选客户自管的外部卷（external volume）存储，在数据保护和计费上有什么区别？

## A
Snowflake 存储：文件由 Snowflake 存储和管理，永久表受 Fail-safe（故障安全保留期）保护，存储费由 Snowflake 收取。外部卷存储：文件在客户自己的 S3/GCS/Azure 存储中，数据保护与恢复由客户负责，Snowflake 不提供 Fail-safe，存储费由云厂商直接向客户收取。两种情况下 Snowflake 都收取查询所用的仓库计算费和云服务费。
