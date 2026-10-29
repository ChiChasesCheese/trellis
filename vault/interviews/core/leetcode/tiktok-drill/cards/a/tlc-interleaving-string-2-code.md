---
id: tlc-interleaving-string-2-code
node: a.interleaving-string
type: qa
step: 2
---
## Q
**LC 97 交错字符串**｜写出 Python 实现

三个小写字母字符串 `s1`、`s2`（长度 `0` 到 `100`）和 `s3`（长度 `0` 到 `200`）。判断 `s3` 能否由 `s1` 与 `s2` 交错组成（各自保序、字符恰好用完）。要求时间 `O(mn)`。

## A
**思路。** `dp[i][j]` 表示 `s1` 的前 `i` 个字符与 `s2` 的前 `j` 个字符能否交错成 `s3` 的前 `i + j` 个字符，`dp[0][0] = True`。逐格填：`s3[i + j - 1]` 来自 `s1[i - 1]`（上一格 `dp[i-1][j]` 为真）或 `s2[j - 1]`（左一格 `dp[i][j-1]` 为真）。答案是 `dp[m][n]`。

```python
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):                    # 长度不等一票否决
        return False
    # dp[i][j]：s1[:i] 与 s2[:j] 能否交错成 s3[:i + j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True                         # 都不取，交错出空串
    for i in range(m + 1):
        for j in range(n + 1):
            if i > 0 and dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]:
                dp[i][j] = True             # s3 的最后一个字符取自 s1
            if j > 0 and dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]:
                dp[i][j] = True             # 或取自 s2
    return dp[m][n]
```

运行：`("aabcc", "dbbca", "aadbbcbcac")` → `True`，`("aabcc", "dbbca", "aadbbbaccc")` → `False`，`("", "", "")` → `True`，`("", "", "a")` → `False`，`("a", "", "a")` → `True`，`("aa", "ab", "aaba")` → `True`。

**复杂度。** 时间 `O(mn)`：每个 `(i, j)` 常数次比较；空间 `O(mn)`：`(m + 1) × (n + 1)` 的布尔表。

**写法要点。** `[[False] * (n + 1) for _ in range(m + 1)]` 每行是一个新列表；两个来源写成两个并列的 `if`，各自带上 `i > 0` / `j > 0` 的边界判断，所以第 0 行、第 0 列不需要单独的初始化循环；`s3[i + j - 1]` 是这一格要匹配的字符；`and` 短路保证 `i == 0` 时不会读 `dp[-1][j]` 或 `s1[-1]`（Python 的负下标不报错，悄悄读到最后一行）。
