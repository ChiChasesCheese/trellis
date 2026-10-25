---
id: tlc-minimum-operations-to-write-the-letter-y-on-a-grid-4-followup
node: b.minimum-operations-to-write-the-letter-y-on-a-grid
type: qa
step: 4
---
## Q
**LC 3071 在矩阵上写出字母 Y 所需的最少操作次数**｜追问

面试官接着问：（1）值域不是 `0..2`，而是 `0..k-1`，`k` 可以很大？（2）形状不是 `Y`，换成别的字母或任意区域？（3）要输出具体应该把格子改成什么？

## A
1. **`k` 很大**：枚举所有 `(a, b)` 是 `O(k^2)`，不必。每个区域只需要考虑出现次数最多的前两个值（出现次数为 `0` 的值也算候选），因为 `a != b` 的冲突最多占用一个区域的最大值：若两个区域的最大值相同，则取（`in` 的最大、`out` 的次大）或（`in` 的次大、`out` 的最大）两者中较优者。这样只比较 `O(1)` 个组合，总复杂度 `O(n^2 + k)`。用 `Counter.most_common(2)` 取前两名，但注意它只返回出现过的值，值不足两个时要自己补上次数为 `0` 的候选。
2. **任意形状**：只需要把“是否在形状上”换成别的判断函数或预先算好的布尔掩码，统计与枚举部分完全不变。形状的定义要先问清楚，例如字母 `X`、`H` 的中心线是否包含中心。
3. **输出方案**：枚举时记下取最小值的 `(a, b)`，再扫一遍矩阵，所有不等于目标的格子就是要修改的位置。

```python
from itertools import permutations


def best_targets(in_y: dict[int, int], out_y: dict[int, int], total: int) -> tuple[int, int, int]:
    """返回 (最少操作数, Y 内目标值, Y 外目标值)。"""
    return min(
        (total - in_y.get(a, 0) - out_y.get(b, 0), a, b)
        for a, b in permutations(range(3), 2)
    )
```

   对示例 1 的统计（`Y` 内 `{1: 3, 2: 1}`，`Y` 外 `{0: 3, 1: 1, 2: 1}`，总数 `9`）得到 `(3, 1, 0)`，即把 `Y` 写成 `1`、背景写成 `0`，共 `3` 次操作。

**Python 提醒**：元组的 `min` 先比第一项再比后续项，把操作数放在首位，并列时按 `(a, b)` 的字典序取，结果可复现；`dict.get(a, 0)` 与 `Counter` 的缺省 `0` 是等价的，函数参数按普通 `dict` 写就两种都能传。
