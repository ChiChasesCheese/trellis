---
id: micro-partition-columnar-inside
node: storage.micro-partition-format
type: qa
source: snowflake-docs
---
## Q
一个微分区（micro-partition）内部的数据是按行还是按列组织的？对一条只引用 3 列的宽表查询有什么影响？

## A
按列组织：表中的一组行被映射进一个微分区，在分区内每一列独立存储（列式存储，columnar storage），并且每列单独压缩，Snowflake 会为每个微分区中的每列自动选择最高效的压缩算法。因此只引用 3 列的查询只扫描这 3 列的数据，其他列即使在同一个微分区里也不会被读取。
