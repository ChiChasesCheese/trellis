---
slug: palindromic-substrings
---
## Q
**LC 647 回文子串**｜Medium

统计字符串中回文子串的个数，位置不同的相同子串分别计数。

## A
**一句话。** 枚举 `2n-1` 个中心（字符和字符之间的缝），向两侧扩展，每扩成功一圈就多一个回文子串。

```python
def count_substrings(s):
    cnt = 0
    for c in range(2 * len(s) - 1):
        l = c // 2
        r = l + c % 2              # 偶数是字符中心，奇数是缝中心
        while l >= 0 and r < len(s) and s[l] == s[r]:
            cnt += 1
            l -= 1
            r += 1
    return cnt
```

**复杂度。** 时间 `O(n²)`，空间 `O(1)`。

**易错点。**
- 只枚举奇数中心：`"aaa"` 得 `4`，应为 `6`。
- 按内容去重：题目按位置计数，`"aaa"` 的答案是 `6` 不是 `3`。

**追问。**
- 能做到线性吗？：Manacher 算法，`O(n)`。
- 用 DP 怎么做？：`dp[i][j] = s[i]==s[j] and dp[i+1][j-1]`，`O(n²)` 空间。

**同模式。** LC 5 最长回文子串、LC 516 最长回文子序列、LC 131 分割回文串
