---
id: hft-architecture-pre-trade-risk-fat-finger-example
node: architecture.pre-trade-risk
type: qa
step: 2
---
## Q
价格合理性检查（fat finger check）具体怎么做？请用小例子说明，并解释为什么实现时用整数乘法而不是除法。

## A
取一个参考价 ref（比如昨收价或最近的中间价）和允许的偏离 bps（1 bp = 0.01%），判断 |px − ref| ≤ ref × bps / 10⁴。

例：ref = 100.00，允许 500 bps（5%），合法价格区间是 95.00–105.00。策略本想以 100.00 卖 1000 股，因 bug 少打了一个 0，报成 10.00：偏离 90.00 > 5.00，被拒绝。若放行，订单会在 10 元成交，白白亏 1000 × 90 = **$90,000**。

实现上价格是定点整数（例如 1 单位 = 0.0001 元），把不等式改写成 `|px − ref| × 10000 ≤ ref × bps`，只用乘法：避免除法的舍入误差，也避免整数除法较慢；乘法若溢出（`Math.multiplyExact` 抛异常）就当作拒绝。
