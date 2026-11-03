---
id: hi-pt-photo-storage-sharing-9-analytics-cdc
node: qb.sd.photo-storage-sharing.points
type: qa
step: 9
---
## Q
**照片存储与分享系统 · 分析与线上隔离**｜追问 · 出自：照片存储与分享系统 › 深入 5

要统计平均照片大小、每个集合平均照片数，为什么不能直接在线上库跑？怎么做？

## A
**问题。** 全库统计要扫描全部分片，拖慢线上请求。
**做法。** CDC 把变更流入数据仓库或 ClickHouse 一类列存，分析在那里跑，延迟几分钟对统计足够。
**实时需求。** 单个集合的实时统计直接读集合行上的计数。
