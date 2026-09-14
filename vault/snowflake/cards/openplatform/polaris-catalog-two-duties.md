---
id: polaris-catalog-two-duties
node: openplatform.polaris-catalog
type: cloze
source: snowflake-docs
---
按 Iceberg 表规范，Iceberg catalog（目录）位于架构的第一层，必须支持两件事：{{c1::存储一张或多张表的当前元数据指针（metadata pointer，把表名映射到当前元数据文件的位置）}}，以及{{c2::原子地更新某张表的当前元数据指针}}。
