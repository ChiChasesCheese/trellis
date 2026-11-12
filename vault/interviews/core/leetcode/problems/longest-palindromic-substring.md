---
slug: longest-palindromic-substring
---
## Q
**LC 5 最长回文子串**｜Medium

求字符串 `s` 中最长的回文子串（连续）。

## A
**一句话。** 枚举 `2n-1` 个中心（字符与缝），从中心向两边扩展到不相等为止。

```python
def longest_palindrome(s):
    n = len(s)
    best_l = best_r = 0
    for center in range(2 * n - 1):
        l = center // 2
        r = l + center % 2     # 偶数：字符中心；奇数：缝中心
        while l >= 0 and r < n and s[l] == s[r]:
            l -= 1
            r += 1
        # 此时回文是 s[l+1 : r]
        if r - l - 1 > best_r - best_l + 1:
            best_l, best_r = l + 1, r - 1
    return s[best_l:best_r + 1]
```

**复杂度。** 时间 `O(n²)`，空间 `O(1)`。

**易错点。**
- 只枚举字符中心：漏掉偶数长回文，`"cbbd"` 得 `"c"`，应为 `"bb"`。
- 长度算成 `r - l + 1`：循环结束时 `l`、`r` 各多走一步，长度是 `r - l - 1`。

**追问。**
- 能 `O(n)` 吗？：Manacher，插分隔符统一奇偶，用最右回文的镜像复用半径。
- 最长回文子序列（LC 516）？：不要求连续，用区间 DP。

**同模式。** LC 647 回文子串、LC 516 最长回文子序列、LC 214 最短回文串、LC 131 分割回文串
