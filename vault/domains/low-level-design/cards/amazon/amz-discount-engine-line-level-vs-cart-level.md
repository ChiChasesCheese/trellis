---
id: amz-discount-engine-line-level-vs-cart-level
node: amazon.amz-discount-engine
type: qa
step: 5
tags: [grown]
---
## Q
在购物车折扣引擎里，满 100 减 10 为什么不能和百分比折扣一样做成「对每一行 apply」？折扣该怎么分层？

## A
两个选项：
- 统一接口 `apply(cart, line)`：灵活，但每个折扣自己决定执行几次，满减被每行各执行一次就多减钱，引擎无法保证钳位。
- 两层接口：`LineDiscount` 只看一行（百分比、买 X 送 Y），`CartDiscount` 只看折后小计，在所有行算完后只执行一次。

选两层，判据是折扣依赖的数据范围。门槛按折后小计判断：原价 120 打八折为 96，不满 100，满减不触发。买 A 送 B 跨两行，只能升到购物车级。
