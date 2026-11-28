---
id: hi-ov-shopify-inventory-reservations-3-when
node: sd.in-the-wild.shopify-inventory-reservations
type: qa
step: 3
tags: [通览]
---
## Q
**Shopify 库存预留 · 能带进面试的**｜通览

Shopify 库存预留能用在哪些面试题上？

## A
**对应的考点。**
- **防超卖与库存预留：** 一个单位一行，加 SKIP LOCKED，是 Ticketmaster 一座一行的生产版。
- **竞争与热点行：** 单行计数让并发买家排队，拆成多行分散锁。
- **跨库一致性：** Redis 与 MySQL 不能一起提交，两阶段提交和 outbox 都没堵住窗口。
- **预留过期：** TTL 删整个计数器，有序集合加后台 worker，或在 MySQL 里按 expires_at 过滤。

**可以怎么引用。** 讲防超卖时说「Shopify 把预留搬进 MySQL，一个单位一行用 SKIP LOCKED，让买家抢不同的行」。被问该不该上 Redis 时，先问预留与账本是否必须同提交。
