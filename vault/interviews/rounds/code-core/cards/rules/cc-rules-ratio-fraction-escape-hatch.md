---
id: cc-rules-ratio-fraction-escape-hatch
node: rules.exact-ratio
type: qa
---
## Q
When is `fractions.Fraction` the right tool instead of hand-rolled cross-multiplication?

## A
**When the ratio has to survive arithmetic, not just a single comparison.**

```python
from fractions import Fraction
r = Fraction(fixed_sessions, total_sessions)      # exact, auto-reduced
fee = Fraction(1500) * r                          # still exact
```

Cross-multiplication is perfect for one `>=`; the moment you multiply ratios, sum them, or carry one through three steps, hand-managed numerators become error-prone. `Fraction` is exact, comparable and hashable, and `Fraction(a, b)` from ints never touches a float.

The costs: it is materially slower than integers in a hot loop, and `Fraction(0.1)` from a float imports the float's error — always construct from ints or a string.

## Q zh
什么时候该用 `fractions.Fraction` 而不是手写交叉相乘？

## A zh
**当比率必须经历运算、而不只是一次比较时。**

```python
from fractions import Fraction
r = Fraction(fixed_sessions, total_sessions)      # exact, auto-reduced
fee = Fraction(1500) * r                          # still exact
```

交叉相乘对付单次 `>=` 完美无缺；一旦你要把比率相乘、相加，或让它经过三步运算，手工维护的分子分母就容易出错。`Fraction` 精确、可比较、可哈希，而由整数构造的 `Fraction(a, b)` 从不碰 float。

代价是：在热循环里明显慢于整数；以及由 float 构造的 `Fraction(0.1)` 会带进 float 的误差 —— 永远用整数或字符串构造。
