---
id: decimal-vs-float-for-money
node: model.numbers
type: qa
source: python-docs
---
## Q
涉及金额计算时为什么推荐用 `decimal.Decimal` 而不是 `float`？`0.1 + 0.1 + 0.1 - 0.3` 在两者下的结果有什么不同？

## A
`Decimal` 内部用十进制系数（coefficient）而不是二进制分数存储数值，能精确表示人类书写的十进制小数：`0.1 + 0.1 + 0.1 - 0.3` 在 `Decimal` 下精确等于 0，而在 `float` 下结果是约 `5.55e-17`（一个非零的微小误差），这种误差会让「金额相等」这类判断变得不可靠，还可能在多次运算里累积。`Decimal` 还会保留有效位数——`Decimal('1.30') + Decimal('1.20')` 得到 `Decimal('2.50')`，末尾的零被保留，这正是货币展示习惯要求的精度语义，`float` 没有这个概念。
