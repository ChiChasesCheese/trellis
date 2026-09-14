---
id: auto-recluster-key-change-cost-traps
node: storage.automatic-reclustering
type: qa
source: snowflake-docs
---
## Q
哪些看似无害的操作会让一张 Snowflake 表突然产生自动聚簇（Automatic Clustering）的 credit 费用，或反而让它停止聚簇？

## A
会产生费用：在已有数据的表上定义聚簇键或修改聚簇键（会触发一次性重新聚簇）；在 `ALTER TABLE ... CLUSTER BY` 中加上 `LINEAR` 关键字，即使列没变也算修改聚簇键，并会恢复自动聚簇；长时间暂停后恢复。会停止聚簇：用 `CREATE TABLE ... CLONE` 克隆出的表（无论克隆的是表、schema 还是数据库），其自动聚簇从暂停状态开始，需要手动 RESUME。
