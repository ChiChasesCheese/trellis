---
id: cache-layers-warmup-cost-comparison
node: cache.cache-layer-tradeoffs
type: qa
tags: [grown]
---
## Q
比较结果缓存和仓库本地磁盘缓存的「预热成本」和「适用面」：为什么说前者命中收益最大但最脆弱，后者收益较小但更通用？

## A
结果缓存（result cache）命中时完全跳过计算，收益最大，但要求查询文本等价、不含非确定性函数且底层数据未变，任何一点不同都无法复用。本地磁盘缓存（local disk cache）只省去从对象存储读取数据的 I/O，仍要重新计算，收益较小；但它按微分区缓存，任何读到同一批分区的不同查询都能受益，代价是需要仓库保持运行才能留住缓存，且挂起或缩容后要重新预热。
