---
id: cc-rules-money-decimal-from-string
node: rules.money
type: qa
---
## Q
You do need a decimal type — a rate table, a proration, an FX product. How do you build and use `Decimal` so it stays exact?

## A
**Construct from the string, quantize with an explicit rounding constant, convert to `int` cents at the end.**

```python
from decimal import Decimal, ROUND_HALF_UP
rate = Decimal("0.021")                       # not Decimal(0.021)
fee  = (Decimal(amount_cents) * rate).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
```

`Decimal(0.021)` inherits the float's error and is exactly as wrong as the float was. `quantize` without a `rounding=` argument uses the context default — `ROUND_HALF_EVEN` — which is banker's rounding and the wrong answer for most fee rules. State the mode every time; the default is never the one you meant. See [[cc-rules-round-half-up-vs-bankers]].

## Q zh
你确实需要小数类型 —— 费率表、按比例分摊、外汇折算。怎么构造和使用 `Decimal` 才能保持精确？

## A zh
**用字符串构造，用显式的 rounding 常量 quantize，最后转成整数分。**

```python
from decimal import Decimal, ROUND_HALF_UP
rate = Decimal("0.021")                       # not Decimal(0.021)
fee  = (Decimal(amount_cents) * rate).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
```

`Decimal(0.021)` 会继承 float 的误差，错得和 float 一模一样。不带 `rounding=` 的 `quantize` 用的是上下文默认值 —— `ROUND_HALF_EVEN`，即银行家舍入 —— 对多数手续费规则来说是错误答案。每次都写明模式；默认值从来不是你想要的那个。见 [[cc-rules-round-half-up-vs-bankers]]。
