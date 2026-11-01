---
id: hi-pt-flight-search-system-9-flex-date
node: qb.sd.flight-search-system.points
type: qa
step: 9
---
## Q
**机票搜索系统 · 弹性日期放大 30 倍**｜出自：机票搜索系统 › 深入 5

「这个月哪天最便宜」的日历视图会让调用量放大约 30 倍，怎么处理？

## A
**做法。** 只在缓存已有的日期上展示价格，或使用供应商的日历接口，其余日期显示「点击查看」；不要为展示一个日历格子逐日调用。
