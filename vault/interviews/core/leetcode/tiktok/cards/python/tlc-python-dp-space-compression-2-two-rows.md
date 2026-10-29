---
id: tlc-python-dp-space-compression-2-two-rows
node: python.dp-space-compression
type: qa
step: 2
---
## Q
**DP 降维｜两行滚动：prev 和 cur**

不同路径（LC 62）的二维表怎样改成只留上一行 `prev` 和本行 `cur`？每个下标怎么对应？

## A
```python
def paths_2d(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]

def paths_two_rows(m: int, n: int) -> int:
    prev = [1] * n                          # 对应 dp[i-1]，先放第 0 行
    for i in range(1, m):
        cur = [1] * n                       # 对应 dp[i]，cur[0] = 1
        for j in range(1, n):
            cur[j] = prev[j] + cur[j - 1]   # dp[i-1][j] + dp[i][j-1]
        prev = cur                          # 本行变成下一轮的上一行
    return prev[-1]

print(paths_2d(3, 7), paths_two_rows(3, 7))     # 28 28
print(paths_2d(18, 18), paths_two_rows(18, 18)) # 2333606220 2333606220
```

- 对应关系：`dp[i-1][j]` → `prev[j]`，`dp[i][j-1]` → `cur[j-1]`，`dp[i][j]` → `cur[j]`。
- 每轮新建 `cur`，轮末 `prev = cur`。写成 `cur = prev` 会让两个名字指向同一个列表，那是下一张卡的"一行原地"。
- 最小路径和（LC 64）同样改：`+` 换成 `min(prev[j], cur[j-1]) + grid[i][j]`，第 0 列单独用 `prev[0] + grid[i][0]`。
- 行也可以是天数、航班趟数：每一轮只读上一轮，就能用两行（LC 188、LC 787）。
