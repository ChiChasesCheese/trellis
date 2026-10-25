---
id: tlc-search-a-2d-matrix-2-code
node: b.search-a-2d-matrix
type: qa
step: 2
---
## Q
**LC 74 搜索二维矩阵**｜写出 Python 实现

`m x n` 矩阵（`1 <= m, n <= 100`，值在 `[-10^4, 10^4]`），每行非严格递增，且每行第一个数大于上一行最后一个数。判断 `target` 是否在矩阵中，时间 `O(log(m * n))`。

## A
**思路。** 把矩阵当作长度 `m * n` 的升序数组，对一维下标做二分。区间 `[lo, hi)`，初值 `[0, m * n)`；取 `mid`，用 `divmod(mid, n)` 得到行列；元素小于 `target` 则 `lo = mid + 1`，否则 `hi = mid`。区间为空后检查 `lo` 位置是否等于 `target`。

```python
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n                      # 把矩阵按行拼成一维有序数组，二分的区间是 [lo, hi)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        row, col = divmod(mid, n)          # 一维下标 -> 行、列
        if matrix[row][col] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo < m * n and matrix[lo // n][lo % n] == target
```

运行：`([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3)` → `True`，`(同一矩阵, 13)` → `False`，`([[1]], 1)` → `True`，`([[1]], 0)` → `False`，`([[1,3]], 3)` → `True`；`100 x 100` 的矩阵中查 `9999` → `True`，查 `10000` → `False`。

**复杂度。** 时间 `O(log(m·n))`，最多约 `14` 轮；空间 `O(1)`。

**写法要点。** `divmod(mid, n)` 一次得到商（行）和余数（列），比分别写 `//` 和 `%` 清楚；除数是列数 `n`，不是行数；沿用 `lo < hi` 的左闭右开模板，退出时 `lo` 是第一个 `>= target` 的位置；最后的 `lo < m * n` 防止 `target` 大于所有元素时越界；整个过程不创建展开后的一维列表，空间 `O(1)`。
