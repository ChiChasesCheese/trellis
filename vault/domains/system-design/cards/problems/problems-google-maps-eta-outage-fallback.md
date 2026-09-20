---
id: problems-google-maps-eta-outage-fallback
node: problems.geo.google-maps
type: qa
step: 6
tags: [grown]
---
## Q
In a Google Maps-style navigation design, if the live traffic aggregation service or the ETA prediction model becomes unavailable, what should the route-planning service do instead of rejecting route requests?

## A
It should degrade to computing ETA from each road segment's static speed limit and historical average speed for that time of day, rather than refusing to serve requests. An ETA with roughly 10-20% more error than the live-traffic-informed prediction is still far more useful to a user trying to navigate than no route at all — the same degrade-gracefully principle used when a spatial index rebuild fails and the system falls back to the last good snapshot rather than going fully unavailable.

## Q zh
在一个类 Google Maps 的导航设计中，如果实时路况聚合服务或 ETA 预测模型不可用，路线规划服务应该怎么做，而不是直接拒绝路线请求？

## A zh
应该降级为用每条路段的静态限速和该时段的历史平均车速来计算 ETA，而不是拒绝服务请求。一个比结合实时路况的预测多出约 10%–20% 误差的 ETA，对一个正在导航的用户来说仍然远比完全无法获得路线有用——这和空间索引重建失败时回退到上一份可用快照、而不是让系统整体不可用，是同一个优雅降级原则。
