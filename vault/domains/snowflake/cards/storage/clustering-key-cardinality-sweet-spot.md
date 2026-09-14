---
id: clustering-key-cardinality-sweet-spot
node: storage.clustering-keys
type: qa
source: snowflake-docs
---
## Q
给 Snowflake 大表选聚簇键（clustering key）时，为什么布尔列 `IS_NEW_CUSTOMER` 和纳秒级时间戳列都是糟糕的候选？该怎么补救后者？

## A
聚簇键的不同值数量（cardinality，基数）要落在中间：足够多才能有效剪枝，足够少才能让相似的行被分到同一批微分区（micro-partition）。布尔列只有两个值，剪枝效果极小；纳秒时间戳几乎每行都不同，无法有效分组，而且基数越高维护聚簇越贵。补救办法是把键定义为保持原有顺序的表达式来降低基数，例如 `to_date(c_timestamp)`，或 `TRUNC(n, -5)` 截断数字——保序才能让每个分区的最小/最大值仍然可用于剪枝。
