---
id: problems-food-delivery-two-consistency-granularities
node: problems.geo.food-delivery
type: qa
step: 2
tags: [grown]
---
## Q
In a design that has to support both a three-sided marketplace variant (independent restaurants, like DoorDash) and a single-party local-inventory variant (platform-owned micro-fulfillment centers, like Gopuff), why do the two variants need fundamentally different mechanisms to prevent overselling, rather than one shared mechanism?

## A
In the marketplace variant, the platform doesn't own a countable stock number for a restaurant's dish — "available" is a coarse flag the merchant sets themselves, and it can lag reality, so the real backstop against overselling is the merchant's explicit order-acceptance step, which can reject an order after the fact. In the local-inventory variant, the platform owns the warehouse and the item count is a precise, countable integer, so overselling has to be prevented with a strongly consistent, conditional decrement on that specific inventory row (an update that only succeeds if quantity is still above zero) — there is no merchant to fall back on for a final check. Applying the marketplace's coarse-flag-plus-acceptance model to the local-inventory variant would let concurrent orders both succeed against the last unit; applying the local-inventory variant's row-level locking to every restaurant menu item would add consistency machinery the marketplace variant has no countable quantity to protect.

## Q zh
在一个既要支持三方市场变体（独立餐厅，类似 DoorDash）、又要支持单一方本地库存变体（平台自持微仓，类似 Gopuff）的设计中，为什么这两种变体防止超卖需要根本不同的机制，而不能共用一套？

## A zh
在市场变体里，平台并不掌握某道菜可数的库存数字——「有货」只是商户自己设置的粗粒度标志，可能落后于真实情况，所以真正防止超卖的兜底是商户显式的接单确认这一步，它可以在事后拒绝订单。在本地库存变体里，平台自己拥有仓储，商品数量是精确可数的整数，所以必须用对那一行库存做强一致的条件扣减（只有数量仍大于零时更新才成功）来防止超卖——这里没有商户可以作为最后一道检查。如果把市场变体「粗粒度标志+接单确认」这套模型套用到本地库存变体上，会让并发订单都对最后一件库存扣减成功；反过来把本地库存变体的行级锁套用到每一道餐厅菜品上，也会为一个根本没有可数库存需要保护的场景引入不必要的一致性机制。
