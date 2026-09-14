---
id: schema-evolution-what-changes-allowed
node: semistructured.schema-evolution-tables
type: qa
tags: [grown]
---
## Q
开启模式演进（schema evolution）后，Snowflake 会自动对表结构做哪两类改动？如果新文件里某个字段的类型从整数变成了字符串，会自动改列类型吗？

## A
自动演进只做两类改动：为新出现的字段添加新列；当新数据中缺少某个带 `NOT NULL` 约束的列时，去掉该列的 NOT NULL 约束。它不会随意修改已有列的数据类型，类型不兼容的数据仍会按加载的错误处理规则报错或被跳过。这些兼容性规则保证了演进只会「放宽」表结构，不会破坏已有数据。
