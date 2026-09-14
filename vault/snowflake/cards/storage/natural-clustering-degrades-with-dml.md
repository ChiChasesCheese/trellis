---
id: natural-clustering-degrades-with-dml
node: storage.natural-vs-explicit-clustering
type: qa
source: snowflake-docs
---
## Q
Snowflake 表不定义聚簇键（clustering key）时也有“自然聚簇”，它从哪里来？什么情况下会变得不够用？

## A
自然聚簇来自数据插入/加载的顺序：例如按日期每天追加的数据，天然就按日期分布在不同的微分区（micro-partition）里，所以 Snowflake 表通常已经聚得不错。它会在两种情况下失效：一是加载时的顺序本身就不理想；二是非常大的表（按数据量而非行数衡量）经历大量 DML 之后，行在期望维度上不再紧凑地聚在一起。
