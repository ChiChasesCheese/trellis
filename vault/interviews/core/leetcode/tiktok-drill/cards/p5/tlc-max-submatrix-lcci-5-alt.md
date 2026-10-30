---
id: tlc-max-submatrix-lcci-5-alt
node: p5.max-submatrix-lcci
type: qa
step: 5
---
## Q
**面试题 17.24 最大子矩阵**｜另一种解法

不用 Kadane，纯粹的二维前缀和暴力怎么写？它在什么规模下可以接受，和压缩成一维的解法怎么选？

## A
**思路。** 先建二维前缀和 `pre`，`pre[r][c]` 是左上角 `r` 行 `c` 列的和，任意子矩阵的和用四个角的前缀和 `O(1)` 求出。再枚举所有上下行对和左右列对，取最大。

```python
from itertools import combinations_with_replacement
from math import inf


def get_max_matrix_brute(matrix: list[list[int]]) -> list[int]:
    rows, cols = len(matrix), len(matrix[0])
    pre = [[0] * (cols + 1) for _ in range(rows + 1)]      # pre[r][c]：左上角 r 行 c 列的和
    for r in range(rows):
        for c in range(cols):
            pre[r + 1][c + 1] = pre[r][c + 1] + pre[r + 1][c] - pre[r][c] + matrix[r][c]
    best, ans = -inf, [0, 0, 0, 0]
    for r1, r2 in combinations_with_replacement(range(rows), 2):
        for c1, c2 in combinations_with_replacement(range(cols), 2):
            s = pre[r2 + 1][c2 + 1] - pre[r1][c2 + 1] - pre[r2 + 1][c1] + pre[r1][c1]
            if s > best:
                best, ans = s, [r1, c1, r2, c2]
    return ans
```

运行：`[[-1,0],[0,-1]]` → `[0,1,0,1]`；`[[1,-2,3],[-4,5,-6],[7,-8,9]]` → `[2,2,2,2]`。

**为什么对。** 子矩阵由 `r1 <= r2`、`c1 <= c2` 唯一确定，`combinations_with_replacement(range(n), 2)` 恰好枚举所有 `i <= j` 的有序对（允许相等，即单行 / 单列）。四角公式是容斥：减去上面和左边，加回重复减去的左上角。

**取舍。** 暴力 `O(R^2 C^2)`：`R = C = 30` 约 `2 * 10^5` 个子矩阵，瞬间完成；`R = C = 200` 约 `4 * 10^8` 个，Python 里跑不完。列压缩 + Kadane 是 `O(R^2 C)`，是面试里的预期解。暴力的价值是写得快、不易错，适合当基准：先写它确认理解，再写优化版并对照。
