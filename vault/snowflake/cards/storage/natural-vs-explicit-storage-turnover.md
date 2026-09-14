---
id: natural-vs-explicit-storage-turnover
node: storage.natural-vs-explicit-clustering
type: qa
source: snowflake-docs
---
## Q
为什么给一张频繁写入的表加显式聚簇键（clustering key）后，存储费用可能明显上涨？旧数据最少要保留多久？

## A
重新聚簇本质是删除受影响的记录再按键分组重新插入，会生成新的微分区（micro-partition）；哪怕只加入少量行，也可能导致包含这些值的所有微分区被重建。被替换的旧微分区只是标记为删除，要等 Time Travel（时间旅行）保留期和随后的 Fail-safe（故障保护）期都过去才清除——最少 8 天，Enterprise 版及以上使用延长 Time Travel 时最多 97 天。数据周转越频繁，同时存在的新旧副本越多。
