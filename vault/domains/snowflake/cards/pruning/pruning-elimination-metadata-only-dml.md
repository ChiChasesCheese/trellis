---
id: pruning-elimination-metadata-only-dml
node: pruning.partition-elimination
type: qa
source: snowflake-docs
---
## Q
为什么“删除表中所有行”这类 DML 操作，在 Snowflake 里可以是一个只操作元数据、不需要重写数据文件的操作？

## A
因为微分区（micro-partition）的元数据已经记录了每个分区归属哪张表、包含哪些行范围等信息，删除全表数据时，引擎只需要把这张表当前指向的所有微分区标记为不再属于该表的最新版本（元数据层面的解绑），而不需要真正读取和重写这些微分区里的底层数据文件，所以是一个元数据级别（metadata-only）的操作。
