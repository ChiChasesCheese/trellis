---
id: ddl-type-widening-vs-rebuild
node: metadata.ddl-metadata-versioning
type: qa
tags: [grown]
---
## Q
在 Snowflake 中把列从 `VARCHAR(50)` 改成 `VARCHAR(200)` 可以直接 ALTER，把 `VARCHAR` 改成 `NUMBER` 却不行，为什么？后者该怎么做？

## A
放宽 VARCHAR 长度（或提高 NUMBER 精度）不改变已存数据的物理表示，所有旧值天然满足新定义，因此只需更新元数据中的列定义，秒级完成。而把字符串改成数字需要逐行转换并可能失败，旧的不可变微分区（micro-partition）里存的仍是字符串，无法仅靠改元数据完成。这类变更需要新建一列或用 `CREATE TABLE ... AS SELECT` 显式转换并重写数据，再切换过去。
