---
id: hi-pt-dasher-payout-4-exact-money
node: qb.lld.dasher-payout.points
type: qa
step: 4
---
## Q
**配送员报酬计算 · 精确算术与舍入**｜必会 · 出自：配送员报酬计算 › 深入 3

金额为什么不能用 `float`，也不要每一段先舍入再相加？内部用什么类型，在哪里舍入？

## A
**类型。** 中间量用 `fractions.Fraction` 精确计算，最后才转 `Decimal` 到分；`float` 连 0.1 都表示不了，`Decimal` 做 `/ 60` 会有循环小数。

**舍入。** 每单只舍入一次。三段各 0.125：每段先舍入成 0.13 得 0.39，整单先加得 0.375 再舍入是 0.38。

```python
def _cents(x: Fraction) -> Decimal:
    return Decimal(int(x * 100 + Fraction(1, 2))).scaleb(-2)
```
