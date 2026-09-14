---
id: micro-partition-drop-column-no-rewrite
node: storage.micro-partition-format
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 中对一张大表执行 `ALTER TABLE ... DROP COLUMN`，为什么语句很快完成，但存储占用却没有立刻下降？

## A
删除列时，包含该列数据的微分区（micro-partition）不会在执行语句时被重写，被删列的数据仍留在存储中。不重写就避免了对整张表的大规模 I/O，所以语句很快；代价是被删列仍然占用存储空间。
