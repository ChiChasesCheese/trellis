---
id: hi-pt-flight-search-system-2-original-flaw
node: qb.sd.flight-search-system.points
type: qa
step: 2
---
## Q
**机票搜索系统 · 原始同步扇出的问题**｜必会 · 出自：机票搜索系统 › 取舍与追问

面试官给出的原始设计是：用户请求同步扇出到所有供应商再合并。它最大的问题是什么？

## A
**问题。** 同步扇出、没有缓存、没有合并、没有预算：延迟取决于最慢供应商；成本与流量线性绑定；供应商限速会直接把用户请求打失败。
