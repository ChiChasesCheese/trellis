---
id: tlc-search-a-2d-matrix-4-followup
node: a.search-a-2d-matrix
type: qa
step: 4
---
## Q
**LC 74 搜索二维矩阵**｜追问

面试官接着问：（1）标准库能不能一行完成二分？（2）矩阵只保证每行每列各自升序（LC 240）怎么办？（3）想返回 `target` 的位置而不是布尔值？

## A
1. **`bisect` + 虚拟数组**：Python 3.10 起 `bisect_left` 支持 `key=`，可以把 `range(m * n)` 当作虚拟的一维数组，`key` 把下标映射成矩阵元素，只对二分探测到的下标调用。

```python
from bisect import bisect_left

def search_matrix_bisect(matrix: list[list[int]], target: int) -> bool:
    m, n = len(matrix), len(matrix[0])
    i = bisect_left(range(m * n), target, key=lambda k: matrix[k // n][k % n])   # range 当作虚拟的一维数组
    return i < m * n and matrix[i // n][i % n] == target
```

示例矩阵查 `3` → `True`，查 `13` → `False`；`range` 不真正占用内存，`key` 只被调用约 `log(m·n)` 次。
2. **LC 240（行列各自有序）**：不能展开。从右上角出发：当前值等于目标就返回；大于目标就列左移，小于目标就行下移；每步排除一行或一列，`O(m + n)`。

```python
def search_matrix_staircase(matrix: list[list[int]], target: int) -> bool:
    row, col = 0, len(matrix[0]) - 1       # 从右上角出发：向左变小，向下变大
    while row < len(matrix) and col >= 0:
        v = matrix[row][col]
        if v == target:
            return True
        if v > target:
            col -= 1
        else:
            row += 1
    return False
```

示例矩阵（也满足 LC 240 的条件）查 `3` → `True`，查 `13` → `False`。
3. **返回位置**：直接返回 `(lo // n, lo % n)`，找不到时返回 `(-1, -1)`；有重复元素时 `lo` 是第一个出现的位置。

**Python 提醒**：`bisect_left` 的 `key` 参数只作用于数组里的元素，**不**作用于被查找的值 `target`，所以 `target` 要保持与 `key` 的返回值同一类型；3.9 及以下没有 `key`，要自己写二分。
