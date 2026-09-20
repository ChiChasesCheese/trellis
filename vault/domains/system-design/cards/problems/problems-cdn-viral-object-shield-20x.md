---
id: problems-cdn-viral-object-shield-20x
node: problems.foundations.cdn
type: qa
step: 6
tags: [grown]
---
## Q
In a CDN with 300 edge PoPs and 15 regional origin shields (20 edges per shield), a single 500MB object suddenly goes viral and every edge PoP misses on it at roughly the same time. Why does adding the shield tier cut the resulting origin egress for this one object from about 146.5GB to about 7.3GB, a 20x reduction, and what does that 20x number equal?

## A
Without a shield, all 300 edge PoPs independently miss and each fetches the full 500MB from origin: 300 x 500MB = 146.5GB of origin egress for one object. With a shield tier, only the 15 shield nodes ever contact origin - each edge's miss is routed to its regional shield first, and the shield coalesces concurrent requests for the same object into a single origin fetch, so origin egress is 15 x 500MB = 7.3GB. The reduction factor (146.5 / 7.3 = 20) is exactly the number of edge PoPs each shield covers (300 edges / 15 shields = 20): the shield's entire value is replacing N independent first-fetches with 1.

## Q zh
在一个有 300 个边缘 PoP 和 15 个区域源站屏蔽层（每个屏蔽层覆盖 20 个边缘）的 CDN 中，一个 500MB 的对象突然爆红，所有边缘 PoP 几乎同时未命中。为什么加入屏蔽层会把这个对象对应的源站出口流量从约 146.5GB 降到约 7.3GB，降低 20 倍？这个 20 倍对应的是什么？

## A zh
没有屏蔽层时，300 个边缘 PoP 各自独立未命中并各自从源站拉取完整的 500MB：300 × 500MB = 146.5GB 的源站出口流量。有了屏蔽层后，只有 15 个屏蔽节点会接触源站——每个边缘的未命中先被路由到它所属的区域屏蔽层，屏蔽层将对同一对象的并发请求合并成一次对源站的请求，所以源站出口流量是 15 × 500MB = 7.3GB。这个降低倍数（146.5 / 7.3 = 20）恰好等于每个屏蔽层覆盖的边缘 PoP 数（300 / 15 = 20）：屏蔽层的价值就是把 N 个独立的首次回源变成 1 个。
