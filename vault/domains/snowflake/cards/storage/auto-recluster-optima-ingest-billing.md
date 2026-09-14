---
id: auto-recluster-optima-ingest-billing
node: storage.automatic-reclustering
type: qa
source: snowflake-docs
---
## Q
Optima Clustering（新一代自动聚簇）怎么计费？为什么按 `TO_DATE(ingestion_time)` 聚簇的只追加（append-only）表几乎不花钱，而频繁改聚簇键列值的表按全价计费？

## A
Optima Clustering 按摄入的数据量计费，而不是按计算小时：费用 = 摄入量 × 重叠因子（overlap factor，0 到 1，表示新数据中需要主动聚簇的比例），上限为每 GB 摄入数据 0.007 credit。按摄入时间聚簇的追加数据天然有序、到达时就聚好，重叠因子接近 0；更新聚簇键取值的数据会与现有微分区（micro-partition）重叠，重叠因子通常为 1，按全价计费。
