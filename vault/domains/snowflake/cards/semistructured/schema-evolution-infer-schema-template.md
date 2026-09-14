---
id: schema-evolution-infer-schema-template
node: semistructured.schema-evolution-tables
type: qa
tags: [grown]
---
## Q
面对一批上千个字段的暂存 Parquet 文件，如何在不手写 DDL 的情况下建出结构化表？这与模式演进怎么配合？

## A
用 `INFER_SCHEMA` 函数检测暂存文件（内部或外部暂存区）中的列定义（列名、数据类型、顺序），再用 `CREATE TABLE … USING TEMPLATE`，以 INFER_SCHEMA 的输出作为模板建表，然后用带 `MATCH_BY_COLUMN_NAME` 的 COPY 加载。INFER_SCHEMA 解决「第一次建表」，开启模式演进后解决「之后新增字段」，二者组合就能让表跟随数据源结构变化。该检测支持 Parquet、Avro、ORC、JSON 和 CSV。
