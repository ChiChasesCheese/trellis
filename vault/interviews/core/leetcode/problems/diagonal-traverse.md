---
slug: diagonal-traverse
---
## Q
**LC 498 对角线遍历**｜Medium

按对角线之字形顺序（先右上、再左下交替）返回 `m×n` 矩阵的所有元素。

## A
**一句话。** 同一反对角线上 `i+j` 相同：按 `i+j` 分组，偶数组反向输出。

```python
def find_diagonal_order(mat):
    m, n = len(mat), len(mat[0])
    diag = defaultdict(list)
    for i, row in enumerate(mat):
        for j, v in enumerate(row):
            diag[i + j].append(v)    # 组内从右上到左下
    res = []
    for d in range(m + n - 1):
        res.extend(diag[d] if d % 2 else reversed(diag[d]))
    return res
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 完全不反向：`[[1,2,3],[4,5,6],[7,8,9]]` 得 `[1,2,4,3,5,7,6,8,9]`，应为 `[1,2,4,7,5,3,6,8,9]`。
- 奇偶写反：起点向右上，所以 `d` 为偶数的组要反向。
- 单行或单列：每条对角线都只含一个元素，别假设至少 `2×2`。

**追问。**
- 能做到 `O(1)` 额外空间吗？：算出每条对角线的行号区间 `[max(0,d-n+1), min(d,m-1)]`，按奇偶决定读取方向。
- 螺旋遍历怎么做？：同样先找边界不变量（LC 54）。

**同模式。** LC 54 螺旋矩阵、LC 59 螺旋矩阵 II、LC 1329 将矩阵按对角线排序、LC 566 重塑矩阵
