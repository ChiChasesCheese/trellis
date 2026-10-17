---
id: amz-discount-engine-how-it-is-asked
node: amazon.amz-discount-engine
type: qa
step: 1
tags: [grown]
---
## Q
Amazon 面试里「购物车折扣引擎（Checkout Price Engine）」怎么问的？开场先问哪三个澄清问题？

## A
被报告的问法：抽象一个 Discount 基类，`isEligible` 判断商品是否适用，`apply` 返回折扣金额；PriceEngine 遍历购物车每一行、依次检查所有折扣、累加后从原价扣除；买 X 送 Y 要把赠品数量乘单价折成减免。

三个问题：
1. 多个折扣能叠加吗？先后顺序如何？（决定是否要有「叠加策略」）
2. 有没有看整车金额的折扣，如满 100 减 10？（决定要不要第二层折扣）
3. 钱用什么表示、有没有多币种？（决定用整数分还是 `Decimal`）
