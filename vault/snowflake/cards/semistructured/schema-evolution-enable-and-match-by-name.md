---
id: schema-evolution-enable-and-match-by-name
node: semistructured.schema-evolution-tables
type: qa
tags: [grown]
---
## Q
上游 Parquet 文件时不时新增字段，希望 Snowflake 表的列跟着自动增长，而不必每次手动 `ALTER TABLE ADD COLUMN`。需要哪两项配置？

## A
1) 在表上设置 `ENABLE_SCHEMA_EVOLUTION = TRUE`，开启表模式演进（table schema evolution）；2) 加载时用 `COPY INTO` 并指定 `MATCH_BY_COLUMN_NAME`，让文件中的字段按列名而不是按位置对应表列。这样当加载的文件中出现表里没有的字段时，Snowflake 会自动为表添加对应的新列。执行加载的角色还需要有修改该表结构的权限。
