---
id: hi-pt-metrics-aggregator-11-percentile-sketch
node: qb.sd.metrics-aggregator.points
type: qa
step: 11
---
## Q
**指标聚合系统 · 分位数草图**｜加分 · 出自：指标聚合系统 › 深入 7

如果仪表盘还要显示延迟的 p99，而不只是计数，聚合方式要怎么改？

## A
**要点。** 分位数不能像计数那样直接相加。每个时间桶存一个分位数草图（如 t-digest），向上降采样时合并草图。

**取舍。** 草图有误差，换来固定的小存储；只做计数时不需要。
