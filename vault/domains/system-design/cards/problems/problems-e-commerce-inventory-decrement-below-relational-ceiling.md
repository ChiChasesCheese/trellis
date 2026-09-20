---
id: problems-e-commerce-inventory-decrement-below-relational-ceiling
node: problems.commerce.e-commerce
type: qa
step: 3
tags: [grown]
---
## Q
In an e-commerce design, ordinary-SKU inventory decrements peak at roughly 136 QPS (850,000 orders/day x 2.3 items/order, x6 peak factor). Why does this number mean you should NOT reach for a Redis atomic-decrement (Lua script) approach by default?

## A
A single managed relational primary is assumed to sustain a few thousand simple conditional updates per second. A peak of ~136 QPS for ordinary inventory is one to two orders of magnitude below that ceiling, so a plain `UPDATE inventory SET stock = stock - qty WHERE stock >= qty` on the relational store is sufficient and simpler to operate. The Redis-Lua atomic-decrement pattern only becomes necessary when a single SKU's contention spikes far above this average — e.g. a flash promotion on one item — at which point that SKU's problem is structurally the flash-sale hot-key problem, not the ordinary checkout path.

## Q zh
在一个电商设计中，普通 SKU 的库存扣减峰值约为 136 QPS（85 万订单/天 × 2.3 件/订单 × 6 倍峰值系数）。为什么这个数字意味着默认不该用 Redis 原子递减（Lua 脚本）方案？

## A zh
一个托管关系型主库被假设能承受每秒几千次简单条件更新。普通库存峰值约 136 QPS，比这个上限低一到两个数量级，所以对关系型存储直接做 `UPDATE inventory SET stock = stock - qty WHERE stock >= qty` 就足够，也更简单。Redis-Lua 原子递减模式只在单个 SKU 的瞬时争用远超这个平均值时才需要——比如某单品的限时促销——这时这个 SKU 的问题在结构上就是秒杀（flash-sale）的热 key 问题，而不是普通结账路径的问题。
