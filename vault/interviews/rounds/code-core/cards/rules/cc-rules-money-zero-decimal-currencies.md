---
id: cc-rules-money-zero-decimal-currencies
node: rules.money
type: qa
---
## Q
An amount field holds `2500`. What does it mean in USD, and what does it mean in JPY?

## A
**$25.00 in USD; ¥2500 in JPY — the minor unit is a property of the currency, not of the number.**

Zero-decimal currencies (JPY, KRW, VND and others) have no subunit, so the integer *is* the amount and printing `¥25.00` is wrong by a factor of a hundred. A few currencies use three decimals.

Consequences: the divisor when rendering, the number of decimals, and the smallest representable step are all per-currency. Keep a table (`{"jpy": 0, "usd": 2}`) and one render function that consults it; never hardcode `/ 100` at the point of printing.

## Q zh
某个金额字段存着 `2500`。它在 USD 里是什么意思？在 JPY 里又是什么意思？

## A zh
**在 USD 里是 $25.00；在 JPY 里是 ¥2500 —— 最小单位是货币的属性，不是数字的属性。**

零小数位货币（JPY、KRW、VND 等）没有辅币单位，所以那个整数**就是**金额，打成 `¥25.00` 会差一百倍。还有少数货币用三位小数。

后果是：渲染时的除数、小数位数、可表示的最小步长，全都是按货币而定的。维护一张表（`{"jpy": 0, "usd": 2}`）和一个查这张表的渲染函数；绝不要在打印处硬写 `/ 100`。
