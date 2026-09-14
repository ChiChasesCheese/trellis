---
id: commit-readers-snapshot-isolation
node: openplatform.external-engine-commit-protocol
type: qa
source: snowflake-docs
---
## Q
一条 Snowflake 查询正在扫描一张 Iceberg 表时，外部引擎提交了一次新的写入。这条查询会读到一半旧数据、一半新数据吗？

## A
不会。Iceberg 采用基于快照的查询模型：查询开始时通过元数据文件和清单文件确定一个快照，它代表表在某个时间点的完整数据文件集合，查询只读这些文件。新提交产生新的快照和新的元数据文件，而旧快照引用的文件不会被原地修改，因此进行中的查询看到的是一致的旧快照，下一次查询才看到新数据，相当于快照隔离（snapshot isolation）。
