---
id: problems-cdn-shield-reduces-origin-qps-5x
node: problems.foundations.cdn
type: qa
step: 1
tags: [grown]
---
## Q
In a CDN design with 300 edge PoPs grouped into 15 regional origin-shield tiers (20 edges per shield), edge cache hit rate is 95% and the regional shield further absorbs 80% of the edge-miss traffic it receives. If peak traffic is 17,361,111 QPS, why does adding the shield tier cut origin QPS from about 868,056 to about 173,611 rather than to zero?

## A
Without a shield, origin sees the full edge-miss rate: 17,361,111 x 0.05 = 868,056 QPS, because every edge PoP that misses goes straight to origin. With a shield, that same 868,056 QPS of edge misses first hits the regional shield, which is itself a cache and absorbs 80% of it (because it aggregates requests from 20 edges, so the same object's misses from many edges collapse into fewer distinct origin-bound requests) - leaving 868,056 x (1 - 0.80) = 173,611 QPS, a 5x reduction. It isn't zero because the shield's own cache still misses on genuinely new or cold content, and that residual miss traffic is exactly what the origin must be sized for.

## Q zh
在一个 CDN 设计中，300 个边缘 PoP 分成 15 个区域源站屏蔽层（origin shield），每个屏蔽层覆盖 20 个边缘节点。边缘命中率 95%，区域屏蔽层对它收到的边缘未命中流量进一步吸收 80%。峰值流量为 17,361,111 QPS 时，为什么加入屏蔽层会把到达源站的 QPS 从约 868,056 降到约 173,611，而不是降为零？

## A zh
没有屏蔽层时，源站看到完整的边缘未命中量：17,361,111 × 0.05 = 868,056 QPS，因为每个未命中的边缘 PoP 都直接回源。有了屏蔽层后，这 868,056 QPS 的边缘未命中先打到区域屏蔽层，屏蔽层本身也是一个缓存，能吸收其中 80%（因为它汇聚了 20 个边缘节点的请求，同一对象在多个边缘的未命中会合并成更少的对源站的请求）——剩下 868,056 × (1 − 0.80) = 173,611 QPS，降低 5 倍。之所以不是零，是因为屏蔽层自己的缓存对真正新或冷门内容仍然会未命中，而这部分残余未命中流量正是源站必须按其容量规划的目标。
