---
id: cc-rules-money-unit-in-the-name
node: rules.money
type: qa
---
## Q
One input column gives amounts as `1000` meaning cents; another gives `10.00` meaning the same money. How do you keep them from mixing?

## A
**Put the unit in the variable name and convert at the boundary, once.**

```python
amount_cents = to_cents(row["amount"])     # accepts "1000" or "10.00"
```

A program where some values are cents and some are units has a bug that arithmetic cannot catch — adding them produces a plausible number. The name is the type system you have: `fee_cents`, `rate_bps`, `allowance_tokens`. Two habits that go with it: convert every incoming amount in the parser, and assert the unit once in the render function, which is the only place the number becomes a decimal again.

## Q zh
一列输入把金额写成 `1000` 表示分；另一列写成 `10.00` 表示同样的钱。怎么防止它们混淆？

## A zh
**把单位写进变量名，并在边界处一次性转换。**

```python
amount_cents = to_cents(row["amount"])     # accepts "1000" or "10.00"
```

一个部分值是分、部分值是元的程序，其 bug 是算术抓不到的 —— 相加会得到一个看起来合理的数。名字就是你手上的类型系统：`fee_cents`、`rate_bps`、`allowance_tokens`。配套的两个习惯：在解析器里转换每一个进来的金额；并在渲染函数里断言一次单位 —— 那是数字重新变回小数的唯一地方。
