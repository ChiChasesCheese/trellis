---
id: mp-metadata-dml-maintenance
node: storage.micro-partition-metadata
type: qa
source: snowflake-docs
---
## Q
DELETE、UPDATE、MERGE 这类 DML 在 Snowflake 中为什么能利用微分区（micro-partition）元数据来简化表维护？举一个极端例子。

## A
元数据记录了每个微分区里有哪些值的范围，DML 可以据此判断哪些微分区与本次操作相关，而不必逐行检查全表。极端情况下，某些操作只需修改元数据即可完成，例如删除表中的全部行，是纯元数据操作（metadata-only operation），无需扫描数据。
