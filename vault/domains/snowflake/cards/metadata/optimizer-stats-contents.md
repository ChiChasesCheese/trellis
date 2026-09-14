---
id: optimizer-stats-contents
node: metadata.optimizer-statistics
type: cloze
source: snowflake-docs
---
Snowflake 优化器可直接使用、无需扫描数据的每微分区（micro-partition）统计信息包括：每列的 {{c1::取值范围}}、每列的 {{c2::不同值数量（number of distinct values）}}，以及其他用于优化和高效查询处理的属性；在表级别还有 {{c3::微分区总数、重叠分区数与重叠深度}} 等聚簇统计。
