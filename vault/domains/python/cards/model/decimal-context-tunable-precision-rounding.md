---
id: decimal-context-tunable-precision-rounding
node: model.numbers
type: qa
source: python-docs
---
## Q
`decimal.Decimal` 的计算精度和舍入方式是固定的吗？和 `float` 由硬件决定的 53 位二进制精度相比有什么不同？

## A
`decimal` 模块的精度由一个用户可调的上下文（context）控制，默认是 28 位十进制有效数字，且可以按需要调大或调小（`getcontext().prec = 6` 之类）；舍入方式也可以在多种模式间选择，比如默认的 `ROUND_HALF_EVEN`（银行家舍入）等。相比之下，`float` 的精度是硬件二进制浮点格式固定给出的（约 53 位二进制有效数字），舍入行为由 IEEE 754 标准和硬件决定，程序员无法像 `Decimal` 那样按需调节精度或指定舍入策略。
