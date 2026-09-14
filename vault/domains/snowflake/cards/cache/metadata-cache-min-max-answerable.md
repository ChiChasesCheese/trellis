---
id: metadata-cache-min-max-answerable
node: cache.metadata-cache-pruning-stats
type: qa
tags: [grown]
---
## Q
`SELECT MIN(order_date), MAX(order_date) FROM orders` 和 `SELECT AVG(amount) FROM orders` 都是全表聚合，为什么前者可以只靠元数据回答，后者却必须扫描数据？

## A
Snowflake 为每个微分区（micro-partition）的每一列保存了最小值/最大值（min/max）统计。全表的 MIN 等于所有分区最小值中的最小者，MAX 同理，因此可以只在元数据上计算。AVG 需要每一行的实际数值来求和，而元数据里没有逐列的总和，所以只能读取数据文件、由仓库计算。
