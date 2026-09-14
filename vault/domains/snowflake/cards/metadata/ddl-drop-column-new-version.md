---
id: ddl-drop-column-new-version
node: metadata.ddl-metadata-versioning
type: qa
tags: [grown]
---
## Q
Snowflake 中 `ALTER TABLE ... DROP COLUMN` 为什么不回收存储？从“元数据版本化”的角度怎么解释？

## A
DROP COLUMN 只是创建一个 schema 中不再包含该列的新表版本，查询按新版本解析时就看不到这列；已有微分区（micro-partition）是不可变文件，不会为了抹掉一列而被重写，被删列的字节仍留在这些文件里。代价换来的是 DDL 的执行时间与表大小无关。
