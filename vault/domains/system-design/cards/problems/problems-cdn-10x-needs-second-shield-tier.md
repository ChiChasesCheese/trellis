---
id: problems-cdn-10x-needs-second-shield-tier
node: problems.foundations.cdn
type: qa
step: 8
tags: [grown]
---
## Q
A CDN designed for 17,361,111 peak QPS across 300 edge PoPs and 15 regional origin shields is scaled 10x to 173,611,111 peak QPS by growing traffic (not by changing the shield topology). Why does the origin start seeing overload again at this scale even though the shield tier's edge-miss-absorption percentage (80%) hasn't changed, and what structural fix restores the original protection?

## A
Origin-bound QPS after the shield is proportional to total peak traffic: at 1x it was about 173,611 QPS, so at 10x traffic with the same edge hit rate and shield absorption percentages, origin-bound QPS scales to about 1,736,111 QPS - ten times what the origin was sized for, because the shield's 80% absorption is a fixed ratio, not a fixed cap. The fix is structural, not just adding origin capacity: insert a second, cross-regional aggregation tier above the 15 regional shields, so shield-tier misses are themselves coalesced across regions before reaching origin, re-creating the same kind of many-to-one funneling that made the first shield tier effective, rather than letting the growth flow straight through to origin.

## Q zh
一个为峰值 17,361,111 QPS、300 个边缘 PoP 、15 个区域源站屏蔽层设计的 CDN，在拓扑不变、流量增长 10 倍到 173,611,111 峰值 QPS 后，即使屏蔽层对边缘未命中流量的吸收比例（80%）没有变，为什么源站会再次面临过载？什么结构性修复能恢复原有的保护效果？

## A zh
经过屏蔽层后到达源站的 QPS 与总峰值流量成正比：1 倍时约为 173,611 QPS，在边缘命中率和屏蔽层吸收比例不变的情况下，流量 10 倍时到达源站的 QPS 也等比放大到约 1,736,111——是源站原本容量的 10 倍，因为屏蔽层 80% 的吸收是一个固定比例而不是固定上限。修复方法是结构性的，而不只是给源站加容量：在 15 个区域屏蔽层之上再加一层跨区域的汇聚层，让屏蔽层自己的未命中在到达源站前先跨区域合并——重建出和第一屏蔽层同样的「多对一」汇聚效果，而不是任由增长直接穿透到源站。
