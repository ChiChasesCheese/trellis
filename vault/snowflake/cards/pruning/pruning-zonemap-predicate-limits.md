---
id: pruning-zonemap-predicate-limits
node: pruning.min-max-zone-maps
type: qa
source: snowflake-docs
---
## Q
为什么一个形如 `WHERE col = (SELECT MAX(x) FROM other_table)` 的谓词，即使子查询结果是个常量，也可能无法触发 zone map 剪枝？

## A
Snowflake 不会基于包含子查询的谓词做剪枝，即便该子查询在运行时会算出一个常量值。原因是剪枝判断发生在查询编译期，此时子查询尚未求值，优化器拿不到具体的比较值去和微分区的 min/max 范围做比较，因此无法在编译期排除任何微分区，只能退化为对该列的运行时扫描。
