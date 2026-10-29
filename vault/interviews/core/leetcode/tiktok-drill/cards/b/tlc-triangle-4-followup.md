---
id: tlc-triangle-4-followup
node: b.triangle
type: qa
step: 4
---
## Q
**LC 120 三角形最小路径和**｜追问

面试官接着问：（1）要输出最小路径本身？（2）题面进阶要求额外空间只有 `O(n)` 呢？（3）自顶向下的写法怎么处理两端？

## A
1. **输出路径**：整张 `dp` 表已经在手，从顶点 `(0, 0)` 出发，每步走到 `dp` 更小的那个后继，不需要额外记录"向下走哪一列"。

```python
def minimum_total_path(triangle: list[list[int]]) -> tuple[int, list[int]]:
    n = len(triangle)
    dp = [[0] * (i + 1) for i in range(n)]
    dp[n - 1] = triangle[n - 1][:]
    for i in range(n - 2, -1, -1):
        for j in range(i + 1):
            dp[i][j] = triangle[i][j] + min(dp[i + 1][j], dp[i + 1][j + 1])
    j, path = 0, [triangle[0][0]]
    for i in range(1, n):                          # 从顶点往下，每步去 dp 更小的后继
        if dp[i][j + 1] < dp[i][j]:
            j += 1
        path.append(triangle[i][j])
    return dp[0][0], path
```

`[[2],[3,4],[6,5,7],[4,1,8,3]]` → `(11, [2, 3, 5, 1])`。
2. **额外空间 `O(n)`（题面进阶）**：空间可以压到 O(n)：见 Python 工具箱「DP 降维」。面试里先写上面的完整二维表，再说压缩。
3. **自顶向下**：`dp[i][j]` 改成"从顶点走到 `(i, j)` 的最小路径和"，`dp[i][j] = triangle[i][j] + min(dp[i-1][j-1], dp[i-1][j])`。每行两端只有一个前驱，每行左右各垫一格 `inf` 就不需要特判；最后取最后一行的最小值。

```python
def minimum_total_top_down(triangle: list[list[int]]) -> int:
    inf = float("inf")
    n = len(triangle)
    dp = [[inf] * (i + 3) for i in range(n)]       # 第 i 行的真实格子在下标 1..i+1，两端是 inf
    dp[0][1] = triangle[0][0]
    for i in range(1, n):
        for j in range(1, i + 2):
            dp[i][j] = triangle[i][j - 1] + min(dp[i - 1][j - 1], dp[i - 1][j])
    return int(min(dp[n - 1]))
```

`[[2],[3,4],[6,5,7],[4,1,8,3]]` → `11`，`[[-10]]` → `-10`。

**Python 提醒**：`dp[-1]` 在 Python 里是最后一个元素而不是越界，自顶向下写 `dp[i][j - 1]` 时 `j = 0` 会悄悄读到末尾；用 `float("inf")` 垫两端比依赖下标回绕可靠。建二维表用 `[[0] * (i + 1) for i in range(n)]`，写成 `[[0] * 3] * 3` 三行会是同一个列表。
