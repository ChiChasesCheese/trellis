---
slug: search-a-2d-matrix
---
## Q
**LC 74 搜索二维矩阵**｜Medium

矩阵每行递增，且每行首元素大于上一行末元素，判断 `target` 是否存在，要求 `O(log(mn))`。

## A
**一句话。** 按行拼起来就是一个升序数组：在虚拟下标 `[0, mn)` 上二分，用 `divmod` 换算行列。

```python
def search_matrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n
    while lo < hi:
        mid = (lo + hi) // 2
        r, c = divmod(mid, n)    # 除数是列数 n
        if matrix[r][c] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo < m * n and matrix[lo // n][lo % n] == target
```

**复杂度。** 时间 `O(log(mn))`，空间 `O(1)`。

**易错点。**
- 换算用了行数 `m`：`2x4` 矩阵里 `mid=4` 得行号 `2`，`IndexError`；除数应是列数 `n`。
- 结束后不检查 `lo < m*n`：`target` 比所有元素大时行号越界。

**追问。**
- 只保证行列各自有序（LC 240）怎么做？：从右上角出发，大了左移、小了下移，`O(m+n)`。
- 能先二分行再二分列吗？：能，`O(log m + log n)`，同阶但边界更易写错。

**同模式。** LC 240 搜索二维矩阵 II、LC 704 二分查找、LC 35 搜索插入位置、LC 378 有序矩阵中第 K 小的元素
