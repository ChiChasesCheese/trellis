---
id: tlc-python-dp-space-compression-5-diagonal
node: python.dp-space-compression
type: qa
step: 5
---
## Q
**DP 降维｜左上角依赖：多存一个变量**

最长公共子序列（LC 1143）压成一行时，左上角 `dp[i-1][j-1]` 会被覆盖，怎么办？不处理会得到什么？

## A
```python
def lcs_2d(a: str, b: str) -> int:
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]

def lcs_1d(a: str, b: str) -> int:
    dp = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        diag = 0                            # dp[i-1][0]
        for j in range(1, len(b) + 1):
            up = dp[j]                      # dp[i-1][j]，马上被覆盖，先存下来
            dp[j] = diag + 1 if a[i - 1] == b[j - 1] else max(up, dp[j - 1])
            diag = up                       # 给下一格 j+1 当左上角
    return dp[-1]

print(lcs_2d("abcde", "ace"), lcs_1d("abcde", "ace"))   # 3 3
print(lcs_2d("a", "aa"), lcs_1d("a", "aa"))             # 1 1
```

- 三个读取：上方 `dp[i-1][j]`（旧）、左边 `dp[i][j-1]`（新）、左上角 `dp[i-1][j-1]`（旧）。左边要新值、左上角要旧值，而它们在数组里是相邻的两格，所以要用变量 `diag` 把旧值留住。
- 不存会错：把 `diag + 1` 写成 `dp[j - 1] + 1`，读到的是本行刚写的新值，`lcs("a", "aa")` 得到 `2`，正确是 `1`。
- 编辑距离（LC 72）同理，`diag` 同样需要。
- 只读左上角、不读左边新值时不需要变量，倒序即可：最长重复子数组（LC 718）写成 `dp[j] = dp[j-1] + 1`，`j` 从大到小。
