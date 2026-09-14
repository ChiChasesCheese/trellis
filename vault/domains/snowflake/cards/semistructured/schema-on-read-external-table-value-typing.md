---
id: schema-on-read-external-table-value-typing
node: semistructured.schema-on-read-parsing
type: qa
source: snowflake-docs
---
## Q
外部表（external table）上，`WHERE value:c1::string = 'foo'` 能用上优化扫描，而 `WHERE value:c1 = 'foo'` 却不能。读时解析的类型在这里起了什么作用？

## A
外部表的每行都以 VARIANT 类型的 `VALUE` 列呈现，字段在查询时才从中解析出来。带显式类型转换的形式 `value:<path>::<type>` 让 Snowflake 事先知道目标类型，可以使用向量化扫描器，并利用 Parquet 行组统计剪枝；不带类型的 `value:c1` 仍是 VARIANT，只能走非向量化扫描器，而且 VARIANT 列不能参与 Parquet 行组剪枝。所以读时模式下，显式声明类型能直接影响性能。
