---
id: external-table-partition-auto-vs-manual
node: ingestion.external-tables-over-lake
type: qa
source: snowflake-docs
---
## Q
外部表的分区可以「自动添加」或「手动添加」。两者分别如何工作？什么时候选择手动方式？

## A
自动方式：建表时把分区列定义为解析 `METADATA$FILENAME` 路径的表达式（如从 `.../date=2026-09-01/` 中取日期），每次刷新元数据时 Snowflake 按表达式计算并加入分区。手动方式：`PARTITION_TYPE = USER_SPECIFIED`，所有者用 `ALTER EXTERNAL TABLE … ADD PARTITION` 有选择地添加或删除分区，不支持自动刷新。需要与 AWS Glue、Hive 等外部元数据存储保持同步时选择手动方式。分区方式在建表后不能更改。
