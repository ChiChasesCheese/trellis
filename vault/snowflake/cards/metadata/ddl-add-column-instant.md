---
id: ddl-add-column-instant
node: metadata.ddl-metadata-versioning
type: qa
tags: [grown]
---
## Q
对一张数 TB 的 Snowflake 表执行 `ALTER TABLE t ADD COLUMN c INT`，为什么几乎瞬间完成？已有行读出来的 c 是什么？

## A
因为这是纯元数据操作：Snowflake 只在元数据中生成带有新列定义的表版本，不重写任何已有的微分区（micro-partition，不可变的列式存储文件）。旧微分区里根本没有 c 这一列的数据，读取时由引擎按新的表定义补出该列的值（未指定默认值时为 NULL）。之后写入的新微分区才会真正包含 c 列。
