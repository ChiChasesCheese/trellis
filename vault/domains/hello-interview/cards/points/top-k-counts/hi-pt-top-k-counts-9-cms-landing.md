---
id: hi-pt-top-k-counts-9-cms-landing
node: qb.sd.top-k-counts.points
type: qa
step: 9
---
## Q
**Top-K 热门榜 · 草图落地与专用存储**｜出自：Top-K 热门榜 › 深入 6

草图放 Redis 还是 Flink 状态？时间序列库、OLAP 库适合 Top-K 吗？

## A
**草图。** Redis CMS 要同时改草图和有序集合，崩溃可能不一致；放 Flink 状态由检查点保护更稳。CMS 不能减法，滑动窗口要自己实现。
**存储。** 时间序列库：对象 ID 作标签有几十亿序列，取前 K 退化为全扫描，不适合；TimescaleDB 本质仍是预聚合加缓存；Druid/Pinot/ClickHouse 写入预聚合，支持任意时间范围，代价是运维复杂。
