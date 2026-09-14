---
id: clustering-key-when-worth-it
node: storage.clustering-keys
type: qa
source: snowflake-docs
---
## Q
什么样的 Snowflake 表值得定义聚簇键（clustering key）？列出应同时满足的条件。

## A
应同时满足：① 表有大量微分区（micro-partition），通常意味着数 TB 数据；② 查询能利用聚簇——查询是选择性的（只读很少比例的行和分区），或者会对数据排序（如 ORDER BY）；③ 大部分查询在同样少数几列上过滤或排序，能共用同一个聚簇键。若目标是降低总成本，还要求查询次数远多于 DML，因为表变动越频繁，保持聚簇越贵。聚簇的初始整理和持续维护都消耗 credit（信用点），所以不适合所有表。
