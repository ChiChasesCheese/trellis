---
id: cc-rules-money-int-float-coercion
node: rules.money
type: qa
tags: [grown]
---
## Q
`price_cents` is a disciplined `int` — `1999` for $19.99. A line of code computes `taxed = price_cents * 1.0825` to apply an 8.25% tax rate written as a literal. What type does `taxed` end up as, and why does this line undo the int-cents discipline without any cast, warning, or error appearing anywhere?

## A
`taxed` becomes a `float`. Multiplying an `int` by a `float` promotes the result to `float` automatically in most languages — the arithmetic follows the less-exact operand as an ordinary rule of numeric promotion, not an error condition, so nothing flags it. Every value on the way into this line was disciplined as an exact integer count of cents, but the moment a bare float literal (`1.0825`) enters the expression, the result silently becomes inexact. The fix is to make the multiplier exact too: build it as a `Decimal` from the string `"1.0825"`, or represent the rate as an integer basis-points value (`10825`) and divide it out explicitly, so no operand in the expression is ever a float.

## Q zh
`price_cents` 是一个遵守纪律的 `int`——$19.99 对应 `1999`。有一行代码计算 `taxed = price_cents * 1.0825`，用一个写成字面量的 8.25% 税率来算税。`taxed` 最终会是什么类型？为什么这一行会在没有任何 cast、警告或报错的情况下，就破坏了 int-cents 的纪律？

## A zh
`taxed` 会变成 `float`。在大多数语言里，`int` 乘以 `float` 会自动把结果提升为 `float`——这只是数值提升的普通规则，跟随精度更低的那个操作数，并不是一种错误条件，所以什么都不会报警。进入这一行之前，每一个值都被严格约束为精确的整数分计数，但一旦表达式里出现一个裸的 float 字面量（`1.0825`），结果就悄悄变得不精确了。修复方法是让乘数也保持精确：用字符串 `"1.0825"` 构造一个 `Decimal`，或者把税率表示成整数的基点值（`10825`）再显式除出来，这样表达式里就没有任何一个操作数是 float。
