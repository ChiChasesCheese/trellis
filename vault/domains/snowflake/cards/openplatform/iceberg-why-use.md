---
id: iceberg-why-use
node: openplatform.iceberg-tables
type: qa
source: snowflake-docs
---
## Q
已经有一个放在 S3 上、被 Spark 等引擎使用的数据湖，为什么选择 Snowflake 的 Apache Iceberg 表（Iceberg table）而不是把数据加载进 Snowflake 原生表？

## A
Iceberg 表把 Snowflake 表的性能和查询语义，与客户自己管理的外部云存储结合起来，适合那些不能或不愿存进 Snowflake 的现有数据湖。数据以开放的 Iceberg 表格式 + Parquet 文件存放，Iceberg 规范本身提供 ACID 事务、模式演进（schema evolution）、隐藏分区（hidden partitioning）和表快照，因此 Snowflake 与其他引擎可以操作同一份数据，而不必维护两份副本。
