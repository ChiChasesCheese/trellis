---
id: explain-partitions-assigned-predict-pruning
node: query.explain-plan-interpretation
type: qa
tags: [grown]
---
## Q
如何用 Snowflake 的 EXPLAIN 输出，在运行查询之前预测剪枝（pruning）效果？

## A
看 GlobalStats 以及各 TableScan 行上的 `partitionsTotal`（表的微分区总数）、`partitionsAssigned`（编译期剪枝后分配给扫描的微分区数）和 `bytesAssigned`（这些分区的字节数）。partitionsAssigned 远小于 partitionsTotal 说明过滤条件能有效剪枝；两者接近说明几乎要全表扫描，应在执行前考虑改写谓词（例如避免对过滤列套函数或用子查询给出过滤值）或调整表的聚簇。
