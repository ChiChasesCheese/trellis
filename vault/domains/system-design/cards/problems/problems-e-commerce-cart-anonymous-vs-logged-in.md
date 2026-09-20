---
id: problems-e-commerce-cart-anonymous-vs-logged-in
node: problems.commerce.e-commerce
type: qa
step: 4
tags: [grown]
---
## Q
In an e-commerce cart design, why does an anonymous cart live in a TTL-bound key-value store while a logged-in cart lives in durable storage, and what happens at the moment of login?

## A
An anonymous shopper has no stable long-lived identity to key a durable record on, and losing an anonymous cart only costs re-adding a few items, so it's kept in a fast, TTL-bound key-value store (e.g. Redis-class, ~30-day TTL) keyed by a device/cookie id. A logged-in cart is durable and keyed by account id. Login triggers a single, explicit merge (not continuous sync): for the same offer, take the larger quantity; for different offers, take the union. Merging once, at a single well-defined moment, avoids having to handle concurrent multi-writer conflicts on the cart in general.

## Q zh
在电商购物车设计中，为什么匿名购物车存在带 TTL 的键值存储里，而登录购物车存在耐久存储里，登录那一刻发生什么？

## A zh
匿名用户没有稳定的长期身份可以作为耐久记录的 key，丢失匿名购物车的代价也只是重新加购几件商品，所以它存在快速的、带 TTL 的键值存储中（Redis 一类，约 30 天 TTL），以设备/cookie id 为 key。登录购物车是耐久的，以账号 id 为 key。登录会触发一次显式合并（不是持续同步）：同一 offer 取数量较大者，不同 offer 取并集。只在一个明确的时刻合并一次，避免了一般情况下处理购物车并发多写冲突的复杂度。
