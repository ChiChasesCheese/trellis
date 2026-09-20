---
id: problems-flash-sale-bottleneck-order
node: problems.commerce.flash-sale
type: qa
step: 2
tags: [grown]
---
## Q
In a flash-sale system, ranking components by their computed safety margin against peak load (from thinnest to thickest), what typically degrades first: uncached origin bandwidth for the product page, an unprotected single Redis inventory instance, or the shared CDN/edge layer?

## A
Uncached origin bandwidth degrades first — if browsing traffic (e.g. 300,000 QPS of page loads/refreshes at 150KB each) isn't served from a CDN, it can demand hundreds of Gbit/s from the origin, which exceeds most origin clusters' capacity outright. An unprotected single Redis instance handling the raw unthrottled purchase-attempt peak comes next, with only a thin margin (about 1.8x over its documented throughput ceiling). The CDN/edge layer is the least likely to degrade, since it's built for exactly this kind of traffic spike and scales horizontally without holding any of the contended state.

## Q zh
在秒杀系统里，按各组件相对峰值负载的计算安全边际从薄到厚排序，商品页未走 CDN 的源站带宽、未受保护的单个 Redis 库存实例、共享的 CDN/边缘层，通常哪个最先扛不住？

## A zh
未走 CDN 的源站带宽最先扛不住——如果浏览流量（比如每次 150KB、峰值 30 万 QPS 的页面加载/刷新）不走 CDN，会对源站产生数百 Gbit/s 的带宽需求，直接超出多数源站集群的承受能力。其次是承受未经限流的裸购买峰值的单个 Redis 实例，安全边际很薄（相对其官方吞吐上限只有约 1.8 倍）。CDN/边缘层最不容易扛不住，因为它天生就是为这类流量脉冲设计的，而且水平扩展时不持有任何被争抢的状态。
