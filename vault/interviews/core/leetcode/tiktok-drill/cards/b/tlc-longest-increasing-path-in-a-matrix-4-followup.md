---
id: tlc-longest-increasing-path-in-a-matrix-4-followup
node: b.longest-increasing-path-in-a-matrix
type: qa
step: 4
---
## Q
**LC 329 矩阵中的最长递增路径**｜追问

面试官接着问：（1）有没有不涉及递归也不涉及出度的写法？（2）要输出具体路径？（3）允许走对角线，或者值可以相等怎么办？

## A
1. **排序后 DP**：把所有格子按值从小到大排序，依次处理；处理到某格时，所有比它小的邻居都已经算好，`length[i][j] = 1 + max(比它小的邻居的 length)`。`O(mn log mn)`，逻辑最直观，也不会爆栈：

```python
from itertools import product


def longest_increasing_path_sorted(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    length = [[1] * n for _ in range(m)]          # length[i][j]：以 (i, j) 结尾的最长递增路径
    cells = sorted(product(range(m), range(n)), key=lambda c: matrix[c[0]][c[1]])
    for i, j in cells:                            # 值从小到大处理：比自己小的邻居一定已经算完
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < m and 0 <= y < n and matrix[x][y] < matrix[i][j]:
                length[i][j] = max(length[i][j], length[x][y] + 1)
    return max(map(max, length))
```

2. **输出路径**：记录每个格子的最优前驱 `prev[i][j]`（取到最大值时的那个邻居），最后从 `length` 最大的格子沿 `prev` 倒着回溯，再反转。
3. **对角线**：只需把方向表扩成八个，其他不变，图仍然是 DAG。**值可相等**（非严格递增）：图里会有环，要先把相等值的连通块缩成一个点再做拓扑 DP，复杂度仍是近线性，但实现复杂得多。

**Python 提醒**：`sorted(..., key=lambda c: matrix[c[0]][c[1]])` 对 `40000` 个格子排序只需几毫秒；`max(map(max, length))` 是对二维表求全局最大值的惯用写法，不需要先展平。
