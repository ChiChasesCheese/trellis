---
id: variant-internal-optimized-format
node: semistructured.variant-type-storage
type: qa
source: snowflake-docs
---
## Q
把 JSON 文件直接加载进一张只有一个 VARIANT 列的表，不指定任何结构。Snowflake 是把原始 JSON 文本当作一个不透明字符串存起来吗？

## A
不是。对于它能识别并解析的格式（JSON、Avro、ORC、Parquet），Snowflake 在加载时解析数据，自动构建层级，并转换为基于 VARIANT、ARRAY、OBJECT 的优化内部存储格式。无论层级是自动构建还是手工指定，最终都是这种内部格式，它专门为快速高效的 SQL 查询而设计，而不是查询时再从头解析文本。
