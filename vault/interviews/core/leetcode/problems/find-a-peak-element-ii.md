---
slug: find-a-peak-element-ii
---
## Q
**LC 1901 寻找峰值 II**｜Medium

`m x n` 矩阵，任意两个相邻格子的值不同。若某格严格大于它上下左右的邻居（越界视为 `-1`）就是峰值。返回任意一个峰值的位置，要求 `O(m log n)` 或 `O(n log m)`。

## A
**一句话。** 对列二分：取中间列的最大值所在行，若它比右边邻居小，右侧一定有峰值，否则峰值在当前列或左侧。

```python
def find_peak_grid(mat):
    def col_max(j):                      # 第 j 列最大值所在行
        return max(range(len(mat)), key=lambda i: mat[i][j])

    lo, hi = 0, len(mat[0]) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        r = col_max(mid)
        if mat[r][mid] < mat[r][mid + 1]:
            lo = mid + 1                 # 右边更大，峰值在右侧
        else:
            hi = mid
    return [col_max(lo), lo]
```

**复杂度。** 时间 `O(m log n)`，空间 `O(1)`。

**易错点。**
- 取中点时不取列最大：只比上下左右会漏掉上下更大的情形，列最大保证上下都不更大。
- 区间写成 `lo <= hi`：`mid + 1` 会越界，这里用 `lo < hi` 且 `hi = mid`。

**追问。**
- 为什么右边一定有峰值？：右半部分的全局最大值不小于 `mat[r][mid+1]`，而 `mat[r][mid+1]` 又大于第 `mid` 列的最大值，所以它的左邻居更小，它就是真峰值。

**同模式。** LC 162 寻找峰值、LC 852 山脉数组的峰顶索引、LC 1095 山脉数组中查找目标值、LC 153 寻找旋转排序数组中的最小值
