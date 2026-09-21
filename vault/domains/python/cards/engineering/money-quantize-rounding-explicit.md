---
id: money-quantize-rounding-explicit
node: engineering.money-time
type: qa
source: python-docs
---
## Q
把 `Decimal('7.325')` 四舍五入到分（两位小数）用于账单展示，为什么不能只调用 `quantize()` 而不传 `rounding` 参数？

## A
`decimal` 模块的默认上下文（context）舍入模式是 `ROUND_HALF_EVEN`（银行家舍入：五时舍入到最近的偶数），不是大多数人以为的「四舍五入」。`quantize(Decimal('.01'))` 不显式传 `rounding` 就会用这个默认模式，结果可能和产品要求的四舍五入不一致。金额场景要显式传入舍入模式，例如 `quantize(Decimal('.01'), rounding=ROUND_HALF_UP)`，把规则写死而不是依赖上下文默认值。
