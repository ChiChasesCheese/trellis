---
id: cc-rules-round-integer-half-up
node: rules.rounding
type: qa
---
## Q
Compute 2.1% of an integer number of cents, rounded half-up, using only integer arithmetic.

## A
**Add half the denominator before the floor division.**

```python
fee = (amount_cents * 21 + 500) // 1000        # 2.1% = 21/1000, half = 500
```

Checks: 1000 → 21; 1234 → 25.914 → 26; **500 → 10.5 → 11** (banker's would give 10); 99 → 2.079 → 2.

The general form for `a * num / den` half-up is `(2 * a * num + den) // (2 * den)`, which stays correct when `den` is odd. This keeps money in `int` end to end, is faster than `Decimal`, and cannot drift — but it is only valid for non-negative values, since `//` floors. See [[cc-rules-round-floor-vs-truncate]].

## Q zh
只用整数运算，计算某个整数分金额的 2.1%，按 half-up 取整。

## A zh
**在整除之前先加上分母的一半。**

```python
fee = (amount_cents * 21 + 500) // 1000        # 2.1% = 21/1000, half = 500
```

核对：1000 → 21；1234 → 25.914 → 26；**500 → 10.5 → 11**（银行家舍入会给 10）；99 → 2.079 → 2。

`a * num / den` 的 half-up 通式是 `(2 * a * num + den) // (2 * den)`，在 `den` 为奇数时也正确。这让钱全程留在 `int` 里，比 `Decimal` 快，也不会漂移 —— 但仅对非负值有效，因为 `//` 是向下取整。见 [[cc-rules-round-floor-vs-truncate]]。
