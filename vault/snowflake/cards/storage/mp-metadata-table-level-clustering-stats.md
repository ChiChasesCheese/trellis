---
id: mp-metadata-table-level-clustering-stats
node: storage.micro-partition-metadata
type: cloze
source: snowflake-docs
---
在表级别，Snowflake 为微分区（micro-partition）维护的聚簇元数据有三项：组成该表的 {{c1::微分区总数}}；在指定列子集上 {{c2::取值范围相互重叠的微分区数量}}；以及这些重叠微分区的 {{c3::深度（depth）}}。
