---
slug: maximum-side-length-of-a-square-with-sum-less-than-or-equal-to-threshold
---
## Q
**LC 1292 元素和小于等于阈值的正方形的最大边长**｜Medium

非负整数矩阵 `mat` 和阈值 `threshold`，求元素和不超过阈值的正方形子矩阵的最大边长，没有返回 `0`。

## A
**一句话。** 二维前缀和 `O(1)` 求任意正方形的和；以每格为右下角，只试「当前答案 + 1」的边长，成功就加一。

```python
def max_side_length(mat, threshold):
    m, n = len(mat), len(mat[0])
    s = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            s[i + 1][j + 1] = (s[i][j + 1] + s[i + 1][j]
                               - s[i][j] + mat[i][j])
    ans = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            k = ans + 1              # 只试比当前答案大一的边长
            if i >= k and j >= k and (
                    s[i][j] - s[i - k][j] - s[i][j - k]
                    + s[i - k][j - k]) <= threshold:
                ans = k
    return ans
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 每格从 1 试到最大：会退化成 `O(mn·min(m,n))`；非负矩阵里只需试 `ans + 1`。
- 前缀和下标差一：`s` 比 `mat` 多一圈 0，正方形和是四个角的容斥。
- 忘了越界判断：`i >= k` 且 `j >= k` 才能取到边长为 `k` 的正方形。

**追问。**
- 为什么只试 `ans + 1` 正确？：矩阵非负，更大的正方形包含边长小一的子正方形，边长只能一格一格增长。
- 另一种思路？：边长二分，边长越大和越大，单调；判定用前缀和 `O(mn)`，总共 `O(mn log)`。

**同模式。** LC 304 二维区域和检索 - 矩阵不可变、LC 221 最大正方形、LC 1314 矩阵区域和
