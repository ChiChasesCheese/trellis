---
id: auto-recluster-optima-suspend-catch-up
node: storage.automatic-reclustering
type: qa
source: snowflake-docs
---
## Q
在 Optima Clustering 下，为了省钱先 `ALTER TABLE ... SUSPEND RECLUSTER`、过段时间再 `RESUME RECLUSTER`，为什么通常不划算？想永久停止付费该怎么做？

## A
暂停时确实立刻停止对新摄入数据计费，但恢复时 Snowflake 会对暂停期间摄入的数据收取补缴（catch-up）费用，钱只是推迟而没有省下。若想永久不再为聚簇付费，应直接删除聚簇键（drop clustering key），这会阻止该表今后的所有重新聚簇。
