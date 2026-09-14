---
id: external-table-readonly-value-column
node: ingestion.external-tables-over-lake
type: qa
source: snowflake-docs
---
## Q
Snowflake 外部表（external table）里的数据存在哪里？它的表结构是怎么来的，能执行 UPDATE 吗？

## A
数据留在外部暂存区指向的云存储中，Snowflake 既不存储也不管理这些文件，只在内部保存文件名、版本标识等文件级元数据。每张外部表都带有一个 VARIANT 类型的 `VALUE` 列（每行对应文件中的一条记录），以及 `METADATA$FILENAME`、`METADATA$FILE_ROW_NUMBER` 两个伪列；创建时只需知道文件格式，不必知道数据模式。外部表是只读的，不能执行 DML，但可以查询、连接和在其上建视图。
