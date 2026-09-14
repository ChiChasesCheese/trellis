---
id: mp-metadata-per-partition-contents
node: storage.micro-partition-metadata
type: cloze
source: snowflake-docs
---
Snowflake 为每个微分区（micro-partition）记录的元数据包括：每列的 {{c1::取值范围（最小值/最大值）}}、{{c2::不同值的数量（distinct count）}}，以及其他用于 {{c3::优化和高效查询处理}} 的属性。
