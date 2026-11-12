---
slug: palindrome-partitioning
---
## Q
**LC 131 分割回文串**｜Medium

把字符串 `s` 分割成若干子串，使每段都是回文，返回所有分割方案。

## A
**一句话。** 先用区间 DP 预处理回文表，再回溯：从 `start` 枚举回文的第一段，递归处理剩下的。

```python
def partition(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]  # s[i..j] 回文
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = (s[i] == s[j] and
                         (j - i < 2 or pal[i+1][j-1]))
    res, path = [], []

    def dfs(start):
        if start == n:
            res.append(path.copy())     # 必须拷贝
            return
        for end in range(start, n):
            if pal[start][end]:
                path.append(s[start:end + 1])
                dfs(end + 1)
                path.pop()

    dfs(0)
    return res
```

**复杂度。** 时间 `O(n · 2^n)`，空间 `O(n^2)`。

**易错点。**
- `res.append(path)` 不拷贝：`"aab"` 最后得 `[[], []]`。
- 填表 `i` 从小到大：`pal[i][j]` 依赖 `pal[i+1][j-1]`，`"aba"` 会漏掉 `["aba"]`。
- 漏掉 `j - i < 2` 特判：长度 1、2 的回文读到越界的内层。

**追问。**
- 最少分割次数（LC 132）？：同一张回文表，再做一维 DP：`dp[j] = min(dp[i-1] + 1)`，`pal[i][j]` 为真。
- 为什么要预处理回文表？：否则每次判回文 `O(n)`，表让判断变成 `O(1)`。

**同模式。** LC 132 分割回文串 II、LC 93 复原 IP 地址、LC 17 电话号码的字母组合、LC 78 子集
