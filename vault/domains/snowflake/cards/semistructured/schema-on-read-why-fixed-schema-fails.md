---
id: schema-on-read-why-fixed-schema-fails
node: semistructured.schema-on-read-parsing
type: qa
source: snowflake-docs
---
## Q
事件日志里，地震记录有 `Magnitude` 字段，龙卷风记录有 `Maximum_wind_speed` 字段，有的记录还缺 `Timestamp`。为什么这类数据适合读时模式（schema-on-read），而不是先定义固定表结构再加载？

## A
关系表要求在加载前定义固定模式（schema），而半结构化数据没有固定模式：新属性随时出现，同一类实体可能有不同属性，属性顺序也不重要，数据还可能不完整。读时模式把原始层级完整保存下来（如存入 VARIANT 列），查询时再按需要的路径取值，因此新增或缺失字段不会导致加载失败，也不必每次改表结构。
