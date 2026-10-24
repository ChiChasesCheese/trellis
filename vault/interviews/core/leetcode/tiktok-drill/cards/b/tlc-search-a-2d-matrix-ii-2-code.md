---
id: tlc-search-a-2d-matrix-ii-2-code
node: b.search-a-2d-matrix-ii
type: qa
step: 2
---
## Q
**LC 240 搜索二维矩阵 II**｜写出 Python 实现

`m x n` 整数矩阵 `matrix`（`1 <= m, n <= 300`，元素与 `target` 都在 `-10^9..10^9`），每行从左到右升序、每列从上到下升序。返回 `target` 是否在矩阵中，要求 `O(m + n)`。

## A
**思路。** 指针从右上角出发。等于目标就返回；当前值大于目标，整列都更大，左移；当前值小于目标，整行都更小，下移。指针走出矩阵说明不存在。

```python
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    row, col = 0, len(matrix[0]) - 1             # 从右上角出发
    while row < len(matrix) and col >= 0:
        cur = matrix[row][col]
        if cur == target:
            return True
        if cur > target:                         # 这一列自上而下递增：cur 往下更大，整列排除
            col -= 1
        else:                                    # 这一行自左而右递增：cur 往左更小，整行排除
            row += 1
    return False
```

**运行。** 例 1（`target = 5`）→ `True`；例 2（`target = 20`）→ `False`；`[[1]], 1` → `True`；`[[1]], 2` → `False`；`[[1,3,5]], 3` → `True`；`[[1],[3],[5]], 4` → `False`。

**复杂度。** 时间 `O(m + n)`：每次循环 `row` 加一或 `col` 减一，两者总共至多走 `m + n` 步；空间 `O(1)`。

**写法要点。** `row, col = 0, len(matrix[0]) - 1` 一行同时定下起点；循环条件 `row < len(matrix) and col >= 0` 同时是越界检查，不需要在循环里再判；三路分支 `==`、`>`、`<`（用 `else` 兜底）每次必走其一，指针必然前进，不会死循环；不修改矩阵。
