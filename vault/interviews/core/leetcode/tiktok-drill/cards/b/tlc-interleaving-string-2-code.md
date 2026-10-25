---
id: tlc-interleaving-string-2-code
node: b.interleaving-string
type: qa
step: 2
---
## Q
**LC 97 交错字符串**｜写出 Python 实现

三个小写字母字符串 `s1`、`s2`（长度 `0` 到 `100`）和 `s3`（长度 `0` 到 `200`）。判断 `s3` 能否由 `s1` 与 `s2` 交错组成（各自保序、字符恰好用完）。要求时间 `O(mn)`，额外空间 `O(len(s2))`。

## A
**思路。** `dp[j]` 表示当前已经用了 `s1` 的前 `i` 个字符、`s2` 的前 `j` 个字符，能否交错成 `s3` 的前 `i + j` 个字符。逐行（`i` 递增）更新：`s3[i + j - 1]` 来自 `s1[i - 1]`（接在上一行同列后面）或 `s2[j - 1]`（接在本行左边一格后面）。

```python
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):                   # 长度不等一票否决
        return False
    # dp[j]：s1 的前 i 个字符与 s2 的前 j 个字符能否交错成 s3 的前 i + j 个字符
    dp = [False] * (n + 1)
    dp[0] = True
    for j in range(1, n + 1):              # i = 0：只能全取自 s2
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, m + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]       # j = 0：只能全取自 s1
        for j in range(1, n + 1):
            k = i + j - 1                  # 要匹配的是 s3[k]
            dp[j] = (dp[j] and s1[i - 1] == s3[k]) or (dp[j - 1] and s2[j - 1] == s3[k])
    return dp[n]
```

运行：`("aabcc", "dbbca", "aadbbcbcac")` → `True`，`("aabcc", "dbbca", "aadbbbaccc")` → `False`，`("", "", "")` → `True`，`("", "", "a")` → `False`，`("a", "", "a")` → `True`，`("aa", "ab", "aaba")` → `True`。

**复杂度。** 时间 `O(mn)`：每个 `(i, j)` 常数次比较；空间 `O(n)`：一个长度 `n + 1` 的布尔数组。

**写法要点。** 原地更新时 `dp[j]` 在赋值前保存的是上一行（`i - 1`）的值，`dp[j - 1]` 已经是本行的值，所以右边的表达式恰好用对了两个来源，不需要临时变量；布尔表达式 `A and B or C and D` 把两个来源写成一行，用括号标清分组；`k = i + j - 1` 单独命名，避免在两处重复写下标算式。
