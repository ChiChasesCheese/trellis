---
slug: maximal-square
---
## Q
**LC 221 最大正方形**｜Medium

在 `'0'`/`'1'` 字符矩阵里找只含 `'1'` 的最大正方形，返回面积。

## A
**一句话。** 二维 DP：`dp[i][j]` 是以该格为右下角的最大边长，等于上、左、左上三格的最小值加一。

```python
def maximal_square(matrix):
    m, n = len(matrix), len(matrix[0])
    # 多一圈 0 作哨兵，dp[i][j] 对应 matrix[i-1][j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    side = 0
    for i, row in enumerate(matrix, 1):
        for j, ch in enumerate(row, 1):
            if ch == "1":
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1],
                                   dp[i-1][j-1])
                side = max(side, dp[i][j])
    return side * side
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 漏掉左上角：`[["1","1","1"],["1","0","1"],["1","1","1"]]` 把右下角算成边长 `2`，应为 `1`。
- 返回边长：题目要面积。
- 元素是字符：写成 `ch == 1` 永远为假，`[["1"]]` 得 `0`。

**追问。**
- 统计所有全 1 正方形（LC 1277）？：把每格的 `dp` 累加，边长 `s` 的右下角贡献 `s` 个。
- 最大矩形（LC 85）？：每行当柱状图的底，用单调栈，`O(mn)`。

**同模式。** LC 1277 统计全为 1 的正方形子矩阵、LC 85 最大矩形、LC 1292 元素和小于等于阈值的正方形的最大边长、LC 62 不同路径
