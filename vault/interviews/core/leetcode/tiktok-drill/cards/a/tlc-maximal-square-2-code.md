---
id: tlc-maximal-square-2-code
node: a.maximal-square
type: qa
step: 2
---
## Q
**LC 221 最大正方形**｜写出 Python 实现

`m × n` 的字符矩阵 `matrix`（`1 <= m, n <= 300`，元素是 `'0'` 或 `'1'`），返回只含 `'1'` 的最大正方形的面积。

## A
**思路。** `dp[j + 1]` 表示以当前行第 `j` 列为右下角的最大正方形边长。每格取左边（刚算完的当前行）、上边（上一行，即覆盖前的 `dp[j+1]`）、左上（上一行的 `dp[j]`，用 `diag` 暂存）的最小值加一；遇到 `'0'` 归零。最后返回最大边长的平方。

```python
def maximal_square(matrix: list[list[str]]) -> int:
    n = len(matrix[0])
    dp = [0] * (n + 1)            # dp[j + 1]：以当前行第 j 列为右下角的最大正方形边长；dp[0] 是左边界哨兵
    side = 0
    for row in matrix:
        diag = 0                  # 左上角（上一行、左一列）的值
        for j, ch in enumerate(row):
            up = dp[j + 1]        # 覆盖之前先存下：它是下一格的左上角
            dp[j + 1] = min(dp[j], up, diag) + 1 if ch == "1" else 0
            diag = up
            side = max(side, dp[j + 1])
    return side * side
```

运行：题面例 1 → `4`，`[["0","1"],["1","0"]]` → `1`，`[["0"]]` → `0`，`[["1"]]` → `1`，`[["1","1","1"],["1","0","1"],["1","1","1"]]` → `1`。

**复杂度。** 时间 `O(mn)`：每格常数次比较；空间 `O(n)`：只保留一行。

**写法要点。** `dp` 长度 `n + 1`，下标 `0` 永远是 `0`，充当左边界，免去 `j == 0` 的分支；`min(a, b, c)` 直接取三者最小；条件表达式 `x if cond else 0` 把「是 `'1'`」和「是 `'0'`」合成一行；`for row in matrix` 加 `enumerate(row)` 不需要用下标取行。`diag = up` 必须放在覆盖之后——先存 `up` 再覆盖，是滚动数组 DP 的固定写法。
