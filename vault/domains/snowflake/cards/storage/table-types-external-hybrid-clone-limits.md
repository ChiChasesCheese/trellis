---
id: table-types-external-hybrid-clone-limits
node: storage.table-types
type: qa
source: snowflake-docs
---
## Q
用 Time Travel（时间旅行）按过去某个时间点克隆整个 schema 或数据库时，外部表（external table）和混合表（hybrid table）会怎样？

## A
外部表不会被克隆；Snowflake 内部 stage 也不会。混合表可以随数据库一起克隆，但不能随 schema 克隆。因此依赖时间点克隆做备份时，这些对象需要另行处理。
