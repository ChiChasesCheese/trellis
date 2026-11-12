---
slug: interleaving-string
---
## Q
**LC 97 交错字符串**｜Medium

判断 `s3` 能否由 `s1` 和 `s2` 交错组成：各自内部字符顺序不变，每次取下一个未用字符，两者恰好用完。

## A
**一句话。** 二维 DP：`dp[i][j]` 表示 `s1[:i]` 与 `s2[:j]` 能否交错成 `s3[:i+j]`，末字符来自 `s1` 或 `s2`。

```python
def is_interleave(s1, s2, s3):
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for i in range(m + 1):
        for j in range(n + 1):
            if i and dp[i-1][j] and s1[i-1] == s3[i+j-1]:
                dp[i][j] = True      # 末字符取自 s1
            if j and dp[i][j-1] and s2[j-1] == s3[i+j-1]:
                dp[i][j] = True      # 末字符取自 s2
    return dp[m][n]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 贪心「能取 `s1` 就取」：`s1="aa"`、`s2="ab"`、`s3="aaba"` 会卡住，答案是 `True`。
- 不先比长度：`("a","b","abc")` 被误判为 `True`。
- `s3` 下标写成 `i+j`：应为 `i+j-1`，错位一格。

**追问。**
- 怎么还原一种交错方案？：从 `(m,n)` 往回看，末字符是 `s1` 还是 `s2` 贡献的。
- 递归记忆化写法？：`go(i, j)` 加 `@cache`，深度 `m+n <= 200` 不会超限。

**同模式。** LC 72 编辑距离、LC 1143 最长公共子序列、LC 115 不同的子序列、LC 10 正则表达式匹配
