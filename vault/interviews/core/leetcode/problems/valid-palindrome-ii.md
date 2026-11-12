---
slug: valid-palindrome-ii
---
## Q
**LC 680 验证回文串 II**｜Easy

最多删除一个字符，字符串能否变成回文。

## A
**一句话。** 对撞双指针：第一次失配时，删左或删右各验证一次剩下的区间是不是回文。

```python
def valid_palindrome(s):
    def is_pal(i, j):             # s[i..j] 闭区间是否回文
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:   # 删左 / 删右各试一次
            return (is_pal(left + 1, right)
                    or is_pal(left, right - 1))
        left += 1
        right -= 1
    return True
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只试删左：`"aab"` 删左得 `"ab"` 不是回文，误判 `False`；删右才对。
- 失配后两边都删（`is_pal(left+1, right-1)`）：`"abc"` 误判 `True`，只能删一个。

**追问。**
- 最多删 `k` 个（LC 1216）？：求最长回文子序列 `lps`，判断 `len(s) - lps <= k`，`O(n^2)` DP。
- 要忽略大小写和非字母数字？：先过滤成小写字母数字，再套同一个函数（LC 125）。

**同模式。** LC 125 验证回文串、LC 5 最长回文子串、LC 1216 验证回文串 III、LC 234 回文链表
