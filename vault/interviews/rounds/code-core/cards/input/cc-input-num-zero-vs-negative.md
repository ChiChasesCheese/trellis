---
id: cc-input-num-zero-vs-negative
node: input.numbers
type: qa
---
## Q
A spec says an amount of `0` is valid but a negative amount makes the command invalid. Name the idiom that quietly gets this wrong.

## A
**`if not amount:` — zero is falsy, so a valid zero takes the invalid branch.** The same trap hides in `if amount:` guards, `amount or default`, and `if not quantity: continue`.

Write the comparison the spec wrote: `if amount < 0: return` for "negative is invalid", `if amount <= 0: return` for "must be positive". They are different rules and both appear: a payment of 0 cents is usually accepted while a refund of 0 is usually rejected. Zero is data, not absence — use `is None` for absence.

## Q zh
题面说金额 `0` 合法，但负数使命令无效。指出会悄悄弄错这一点的写法。

## A zh
**`if not amount:` —— 零是假值，于是合法的零走进了非法分支。** 同样的坑还藏在 `if amount:` 保护、`amount or default`、`if not quantity: continue` 里。

按题面写的比较来写：「负数无效」就写 `if amount < 0: return`，「必须为正」就写 `if amount <= 0: return`。这是两条不同的规则，而且都会出现：0 分的付款通常被接受，0 元的退款通常被拒绝。零是数据，不是缺失 —— 缺失请用 `is None` 判。
