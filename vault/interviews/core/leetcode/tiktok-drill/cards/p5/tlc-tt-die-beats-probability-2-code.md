---
id: tlc-tt-die-beats-probability-2-code
node: p5.tt-die-beats-probability
type: qa
step: 2
---
## Q
**一个骰子掷出更大点数的概率**｜写出 Python 实现

两个公平骰子 `A`、`B`（面数各 `<= 10^5`，面上的数在 `±10^9`，可重复），各掷一次，返回 `A` 严格大于 `B` 的精确概率。

## A
**思路。** 概率 = 赢的组合数 / `p·q`。`B` 排序后，`bisect_left(sorted_b, x)` 就是 `B` 中严格小于 `x` 的面数；对 `A` 的每一面求和得到赢的组合数，用 `Fraction` 返回。

```python
from bisect import bisect_left
from fractions import Fraction


def beat_probability(a: list[int], b: list[int]) -> Fraction:
    sorted_b = sorted(b)
    # 对 A 的每一面，数 B 中严格小于它的面：bisect_left 返回 < x 的个数
    wins = sum(bisect_left(sorted_b, x) for x in a)
    return Fraction(wins, len(a) * len(b))
```

运行：`A = [2,2,6]`，`B = [1,5,5]` → `Fraction(5, 9)`；`A = [1,5,5]`，`B = [2,2,6]` → `4/9`；`[3]` 对 `[3]` → `0`；`[-10^9]` 对 `[10^9]` → `0`。

**复杂度。** 时间 `O(q log q + p log q)`；空间 `O(q)`（排序副本）。

**写法要点。** `bisect_left` 返回第一个 `>= x` 的位置，也就是 `< x` 的元素个数，`bisect_right` 则是 `<= x` 的个数，两者之差是等于 `x` 的个数；`sum` 配生成器表达式不建中间列表；`Fraction(分子, 分母)` 自动约分，比较相等是精确的；`sorted(b)` 返回新列表，不修改调用者的输入。
