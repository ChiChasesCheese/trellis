---
id: cc-python-pitfalls-float-equality
node: python.pitfalls
type: qa
---
## Q
`0.1 + 0.2 == 0.3` is `False`, and a running total of a million float amounts is off by a few units. Name the two distinct problems and the fix for each.

## A
**Representation error and accumulation error — they are not the same bug.**

- **Representation**: binary floating point cannot hold most decimal fractions, so `0.1 + 0.2` is `0.30000000000000004`. Never compare floats with `==`; use `math.isclose(a, b, rel_tol=1e-9)` when the quantity is genuinely physical.
- **Accumulation**: every addition rounds, so a million additions drift. Money and counts belong in `int` minor units or `Decimal`; a ratio test should cross-multiply integers (`a * d >= c * b`) rather than divide.
- A float holding whole numbers is exact only up to 2^53; past that `float(n) == float(n + 1)`.

## Q zh
`0.1 + 0.2 == 0.3` 是 `False`，而一百万个浮点金额累加出来的总数差了几个单位。说出这两个不同的问题，以及各自的修法。

## A zh
**表示误差和累积误差 —— 它们不是同一个 bug。**

- **表示**：二进制浮点装不下大多数十进制小数，所以 `0.1 + 0.2` 是 `0.30000000000000004`。绝不要用 `==` 比较浮点；当这个量确实是物理量时用 `math.isclose(a, b, rel_tol=1e-9)`。
- **累积**：每次加法都舍入，一百万次加法就会漂移。金额和计数应放在 `int` 最小单位或 `Decimal` 里；比例判断应当交叉相乘整数（`a * d >= c * b`）而不是做除法。
- 装整数的浮点只在 2^53 以内精确；再往上 `float(n) == float(n + 1)`。
