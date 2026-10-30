---
id: tlc-minimum-operations-to-write-the-letter-y-on-a-grid-2-code
node: b.minimum-operations-to-write-the-letter-y-on-a-grid
type: qa
step: 2
---
## Q
**LC 3071 在矩阵上写出字母 Y 所需的最少操作次数**｜写出 Python 实现

`n x n` 矩阵 `grid`（`3 <= n <= 49`，`n` 为奇数，值为 `0`、`1`、`2`）。`Y` 由从左上、右上两个角到中心的对角线，加上从中心到底边的竖线组成。要使 `Y` 内的格子值全相等、`Y` 外的格子值全相等、且两个值不同，每次操作可改一个格子的值，返回最少操作次数。

## A
**思路。** 扫一遍矩阵，用两个 `Counter` 分别统计 `Y` 内、`Y` 外各值的出现次数。枚举有序对 `(a, b)`，`a != b`，操作数是 `n * n - in_y[a] - out_y[b]`，取最小。

```python
from collections import Counter
from itertools import permutations


def minimum_operations_to_write_y(grid: list[list[int]]) -> int:
    n = len(grid)
    mid = n // 2
    in_y: Counter[int] = Counter()         # Y 上各个值的出现次数
    out_y: Counter[int] = Counter()        # Y 外各个值的出现次数
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            on_y = (r <= mid and (c == r or c == n - 1 - r)) or (r > mid and c == mid)   # 两条对角线（到中心）+ 竖线（中心以下）
            (in_y if on_y else out_y)[v] += 1
    # Y 内统一成 a，Y 外统一成 b，且 a != b；改动数 = 总格数 - 已经正确的格数
    return min(n * n - in_y[a] - out_y[b] for a, b in permutations(range(3), 2))
```

运行：`[[1,2,2],[1,1,0],[0,1,0]]` → `3`，`[[0,1,0,1,0],[2,1,0,1,2],[2,2,2,0,1],[2,2,2,2,2],[2,1,2,2,2]]` → `12`，全 `1` 的 `3 × 3` → `4`，全 `0` 的 `3 × 3` → `4`。

**复杂度。** 时间 `O(n^2)`：扫描 `n^2` 个格子，加 `6` 个常数组合；空间 `O(1)`。

**写法要点。** `(in_y if on_y else out_y)[v] += 1` 用条件表达式选出要更新的计数器，省掉 `if / else` 两个分支；`Counter` 对不存在的键返回 `0`，所以值没出现过也不用判断；`permutations(range(3), 2)` 恰好生成 `a != b` 的 `6` 个有序对，把“两个值不同”直接编码在枚举里；`r <= mid` 的判断里中心格同时满足 `c == r` 和 `c == n - 1 - r`，用 `or` 只算一次。
