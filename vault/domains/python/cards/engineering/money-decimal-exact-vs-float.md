---
id: money-decimal-exact-vs-float
node: engineering.money-time
type: qa
source: python-docs
---
## Q
用 `Decimal` 计算 `0.1 + 0.1 + 0.1 - 0.3`，结果和 `float` 版本有什么不同？为什么金额计算要用 `Decimal`？

## A
`Decimal` 版本精确等于 0，`float` 版本因为二进制浮点（binary floating point）无法精确表示十进制小数，结果是约 5.55e-17 这样的极小非零值。金额计算反复累加会放大这类误差，破坏「借贷相等」这种严格相等性校验，所以会计场景优先用 `Decimal`（十进制浮点）而不是 `float`。
