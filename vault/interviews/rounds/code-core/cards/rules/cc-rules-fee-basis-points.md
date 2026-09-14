---
id: cc-rules-fee-basis-points
node: rules.fees
type: qa
---
## Q
A rate table gives rates in basis points: `card,ie,140,25`. Compute the fee, and say why you must not reuse the default rule's rounding.

## A
**`amount_cents * bps // 10000 + fixed`, floored — because the table's spec says floor while the default rule says half-up.**

```
1000 x 140 bps // 10000 + 25 = 14 + 25 = 39
500  x 290 bps // 10000 + 0  = 14         (14.5 floored, not 15)
```

Two rules with two rounding modes in the same program is normal and deliberate; unifying them "for consistency" changes answers on every tie. Keep each rule's rounding at its own call site, name the modes, and be sure the table applies only where the statement says — typically to completed payments, never to dispute fees.

## Q zh
费率表以基点给出费率：`card,ie,140,25`。算出手续费，并说明为什么不能沿用默认规则的取整方式。

## A zh
**`amount_cents * bps // 10000 + fixed`，向下取整 —— 因为表的规格说 floor，而默认规则说 half-up。**

```
1000 x 140 bps // 10000 + 25 = 14 + 25 = 39
500  x 290 bps // 10000 + 0  = 14         (14.5 floored, not 15)
```

同一个程序里两条规则用两种取整是正常且刻意的；为了"一致性"把它们统一，会在每个平局上改变答案。让每条规则的取整留在它自己的调用点，写明模式，并确认这张表只在题面说的地方生效 —— 通常只对已完成的付款，绝不对争议费。
