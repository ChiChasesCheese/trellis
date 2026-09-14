---
id: cc-transfer-quant-numerical-care
node: transfer.quant
type: qa
---
## Q
A simulation over 10^6 paths returns a probability of exactly 0 and a variance that is negative. Name the two numerical failures and the fixes.

## A
**Underflow from multiplying many small probabilities, and catastrophic cancellation in a one-pass variance.**

- Work in **log space**: accumulate `math.log(p)` instead of multiplying, and exponentiate only at the end (`math.fsum` for the sum, `logsumexp` when you must add probabilities).
- Never compute variance as `E[X²] − E[X]²` in floating point — the two terms are nearly equal, so the difference is all rounding error. Use Welford's online update or `statistics.variance`.
- Use `fractions.Fraction` for small combinatorial answers: exact, and it removes the question of whether `0.16666666` should have been `1/6`.
- Sanity-check every number against a bound — a probability in [0, 1], a variance ≥ 0, an expectation between the smallest and largest outcome.

## Q zh
一个跑了 10^6 条路径的模拟返回了恰好为 0 的概率和一个负的方差。说出这两处数值失败和修法。

## A zh
**大量小概率连乘造成的下溢，以及单遍方差公式里的灾难性抵消。**

- 在**对数空间**里工作：累加 `math.log(p)` 而不是连乘，只在最后取指数（求和用 `math.fsum`，必须相加概率时用 `logsumexp`）。
- 绝不要用浮点算 `E[X²] − E[X]²` —— 两项几乎相等，差值全是舍入误差。改用 Welford 在线更新或 `statistics.variance`。
- 小规模组合问题用 `fractions.Fraction`：精确，并且免去了「`0.16666666` 是不是本该是 `1/6`」这个问题。
- 每个数字都对着一个界做合理性检查 —— 概率落在 [0, 1]、方差 ≥ 0、期望落在最小与最大结果之间。
