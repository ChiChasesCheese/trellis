---
id: tlc-maximum-of-absolute-value-expression-4-followup
node: a.maximum-of-absolute-value-expression
type: qa
step: 4
---
## Q
**LC 1131 绝对值表达式的最大值**｜追问

面试官接着问：（1）要返回取到最大值的下标对 `(i, j)`？（2）推广到 `k` 个数组？（3）能不能 `O(1)` 额外空间？

## A
1. **返回下标对**：每种符号组合记录 `argmax` 和 `argmin`，差值最大的那组给出 `(i, j)`（`f(i)` 最大、`f(j)` 最小）：

```python
from itertools import product


def max_abs_val_pair(arr1: list[int], arr2: list[int]) -> tuple[int, int, int]:
    best = (0, 0, 0)                       # (最大值, i, j)
    for p, q in product((1, -1), repeat=2):
        vals = [p * a + q * b + i for i, (a, b) in enumerate(zip(arr1, arr2))]
        hi = max(range(len(vals)), key=vals.__getitem__)
        lo = min(range(len(vals)), key=vals.__getitem__)
        if vals[hi] - vals[lo] > best[0]:
            best = (vals[hi] - vals[lo], hi, lo)
    return best
```
   运行：示例 1（`[1,2,3,4]`、`[-1,4,5,6]`）→ `(13, 3, 0)`，即 `|4-1| + |6-(-1)| + |3-0| = 13`。
2. **`k` 个数组**：点是 `(k + 1)` 维，符号组合 `2^(k+1)` 种，固定一维符号后 `2^k` 种，每种 `O(nk)`，总计 `O(2^k · n · k)`；`k` 很小才划算。
3. **`O(1)` 额外空间**：不建 `vals` 列表，边扫边更新 `hi`、`lo` 两个变量，每种组合一次循环：`hi = max(hi, v)`，`lo = min(lo, v)`。

**Python 提醒**：`max(range(n), key=vals.__getitem__)` 返回最大值的**下标**；有多个并列最大时返回第一个。`max(vals)` 与 `vals.index(max(vals))` 效果相同但扫描两遍。
