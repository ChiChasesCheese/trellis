---
id: amz-discount-engine-how-it-is-asked
node: amazon.amz-discount-engine
type: qa
step: 1
tags: [grown]
---
## Q
购物车折扣引擎（Checkout Price Engine）要你设计什么？开场先问哪三个澄清问题？

## A
要设计的是一个算购物车总价的引擎：抽象一个 Discount 基类，`isEligible` 判断商品是否适用，`apply` 返回折扣金额；PriceEngine 遍历购物车每一行、依次检查所有折扣、累加后从原价扣除；买 X 送 Y 不直接减钱，要把赠品数量乘单价折成减免。

三个问题：
1. 多个折扣能叠加吗？先后顺序如何？答「能叠加」就要定顺序，答「只取最划算的」就要多一条选最大的策略。
2. 有没有看整车金额的折扣，如满 100 减 10？有的话，折扣要分成「只看一行」和「看整车」两层，因为满减若放进逐行循环会被扣多次。
3. 钱用什么表示、有没有多币种？浮点数会差几分钱，所以用整数分；多币种则要另加货币类。
