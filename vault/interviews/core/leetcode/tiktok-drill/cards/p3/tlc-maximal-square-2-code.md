---
id: tlc-maximal-square-2-code
node: p3.maximal-square
type: qa
step: 2
---
## Q
**LC 221 最大正方形**｜写出 Python 实现

`m × n` 的字符矩阵 `matrix`（`1 <= m, n <= 300`，元素是 `'0'` 或 `'1'`），返回只含 `'1'` 的最大正方形的面积。

## A
**思路。** `dp[i][j]` 表示以矩阵第 `i-1` 行第 `j-1` 列为右下角的最大正方形边长；表多一行一列全 `0` 的哨兵。每格是 `'1'` 时取上、左、左上三个邻居的最小值加一，是 `'0'` 时保持 `0`；一边填一边记最大边长，最后返回它的平方。

```python
def maximal_square(matrix: list[list[str]]) -> int:
    m, n = len(matrix), len(matrix[0])
    # dp[i][j]：以 matrix[i-1][j-1] 为右下角的最大全 1 正方形边长；第 0 行、第 0 列是哨兵 0
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    side = 0
    for i, row in enumerate(matrix, 1):
        for j, ch in enumerate(row, 1):
            if ch == "1":
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                side = max(side, dp[i][j])
    return side * side
```

运行：题面例 1 → `4`，`[["0","1"],["1","0"]]` → `1`，`[["0"]]` → `0`，`[["1"]]` → `1`，`[["1","1","1"],["1","0","1"],["1","1","1"]]` → `1`，`300×300` 全 `"1"` → `90000`。

**复杂度。** 时间 `O(mn)`：每格常数次比较；空间 `O(mn)`：`(m + 1) × (n + 1)` 的表。

**写法要点。** 表多一行一列哨兵 `0`，`dp[i - 1][j]`、`dp[i][j - 1]`、`dp[i - 1][j - 1]` 在第一行、第一列也合法，免去 `i == 0 or j == 0` 的分支；`enumerate(matrix, 1)` 和 `enumerate(row, 1)` 让 `i`、`j` 直接是表里的下标；`min(a, b, c)` 直接取三者最小；`'0'` 的格子不用写 `else`，表里本来就是 `0`；在填表时顺便维护 `side`，不用再扫一遍。
