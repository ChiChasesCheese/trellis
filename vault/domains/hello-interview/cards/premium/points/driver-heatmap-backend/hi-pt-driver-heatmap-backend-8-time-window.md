---
id: hi-pt-driver-heatmap-backend-8-time-window
node: qb.sd.driver-heatmap-backend.points
type: qa
step: 8
---
## Q
**司机热力图 · 时间窗口**｜追问 · 出自：司机热力图 › 深入 5

司机热力图要支持"过去 20 分钟"的窗口。怎么存、怎么查？存储多大？

## A
**做法。** 每分钟存一份各层计数快照，窗口查询取 20 份聚合（平均或最大）。

**存储。** (67 万 + 2.1 万 + 660) 个格 × 20 B ≈ 14 MB/分钟，一天 1,440 分钟约 20 GB，只存非零格更小。

**近似。** 各分钟相加会重复计数换格的司机，热力图可接受；要精确去重才需要 HyperLogLog。
