---
id: cc-rules-fee-percent-plus-fixed
node: rules.fees
type: qa
---
## Q
Implement the classic "2.9% + 30¢" fee on an integer-cent amount, and say what it charges on an amount of 0.

## A
**Percentage first, rounded as specified, then the fixed part added — and 0 still costs 30.**

```python
fee = (amount_cents * 29 + 500) // 1000 + 30      # 2.9% half-up, + 30c
```

The fixed component is unconditional: a completed payment of zero still attracts the fixed fee, which is a documented edge case and a common wrong answer (`if not amount: return 0`).

Order matters too: rounding applies to the percentage alone, so `+ 30` sits outside the rounding. Rounding the sum instead is a different rule and gives different totals whenever the percentage lands on a tie.

## Q zh
在整数分金额上实现经典的「2.9% + 30¢」手续费，并说出金额为 0 时收多少。

## A zh
**先算百分比、按规定取整，再加固定部分 —— 而 0 仍要收 30。**

```python
fee = (amount_cents * 29 + 500) // 1000 + 30      # 2.9% half-up, + 30c
```

固定部分是无条件的：金额为零的已完成付款照样收固定费，这是有明确记载的边界情形，也是常见的错误答案（`if not amount: return 0`）。

顺序同样要紧：取整只作用于百分比部分，所以 `+ 30` 在取整之外。改成对总和取整是另一条规则，只要百分比落在平局上就会给出不同的总额。
