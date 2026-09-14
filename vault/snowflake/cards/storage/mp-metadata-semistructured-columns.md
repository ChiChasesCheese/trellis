---
id: mp-metadata-semistructured-columns
node: storage.micro-partition-metadata
type: qa
source: snowflake-docs
---
## Q
表里有一列存放 JSON 等半结构化数据（semi-structured data），过滤这列里的字段时，Snowflake 还能用微分区（micro-partition）元数据做剪枝吗？

## A
能。Snowflake 维护的微分区元数据支持在查询运行时对微分区中的列做精确剪枝，其中包括存放半结构化数据的列。因此半结构化列并不天然意味着全表扫描，只要元数据能证明某个微分区不含目标值，它就会被跳过。
