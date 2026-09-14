---
id: cc-input-num-float-loses-digits
node: input.numbers
type: qa
---
## Q
Token counts reach 10^9 and ledger amounts reach 10^12 cents. Why is `float(tok)` a bug even when you never print a decimal?

## A
**A float carries 53 bits of mantissa: integers above 2^53 ≈ 9·10^15 stop being representable, and every arithmetic step before that can already drift.**

Python's `int` is arbitrary precision, so `int(tok)` and integer arithmetic are exact at any size — there is no reason to leave that. Concretely: summing a million float cents accumulates error that flips one final rounding; `float("12345678901234567890")` loses the low digits outright. Parse to `int`, keep the whole computation in `int`, and convert to a decimal string only at the render step.

## Q zh
token 数达到 10^9，账本金额达到 10^12 分。即使你从不打印小数，为什么 `float(tok)` 仍是 bug？

## A zh
**float 只有 53 位尾数：超过 2^53 ≈ 9·10^15 的整数就无法精确表示，而在此之前的每一步运算就已经可能漂移。**

Python 的 `int` 是任意精度的，`int(tok)` 和整数运算在任何规模下都精确 —— 没有理由放弃它。具体地说：把一百万个 float 分相加，累积误差足以翻转最后一次取整；`float("12345678901234567890")` 则直接丢掉低位。解析成 `int`，整个计算保持 `int`，只在渲染那一步转成小数字符串。
