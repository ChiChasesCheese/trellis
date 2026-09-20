---
id: problems-e-commerce-five-consistency-domains
node: problems.commerce.e-commerce
type: qa
step: 1
tags: [grown]
---
## Q
In an e-commerce checkout design, why is it a mistake to treat the catalogue, cart, checkout/inventory, and order as one consistency model instead of picking a guarantee per domain?

## A
Each domain needs a different trade-off: the product catalogue is read at a ratio of roughly 1,400 reads per order in a typical design, so it must be served from cache/CDN and tolerates seconds of staleness (eventual consistency); inventory decrement at checkout must never oversell, so it needs a strongly-consistent conditional update; the cart tolerates conflicts resolved by a merge; and the order, once created, must never be lost, driving downstream work through a durable saga. Forcing one model onto all of them either makes the read path too expensive (strong consistency everywhere) or lets inventory oversell (eventual consistency everywhere).

## Q zh
在电商结账设计中，为什么把目录、购物车、结账/库存、订单当成同一种一致性模型而不是按域各自选择保证是一个错误？

## A zh
每个域需要不同的权衡：商品目录在典型设计中每笔订单大约对应 1,400 次读，所以必须走缓存/CDN 服务且容忍秒级陈旧（最终一致）；结账时的库存扣减绝不能超卖，需要强一致的条件更新（conditional update）；购物车容忍冲突、靠合并解决；订单一旦创建绝不能丢失，需要通过持久化的 saga 驱动下游。给全部域套同一种模型，要么让读路径代价过高（处处强一致），要么让库存超卖（处处最终一致）。
