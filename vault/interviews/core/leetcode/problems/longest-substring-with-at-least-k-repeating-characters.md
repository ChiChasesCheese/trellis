---
slug: longest-substring-with-at-least-k-repeating-characters
---
## Q
**LC 395 至少有 K 个重复字符的最长子串**｜Medium

给字符串 `s` 和整数 `k`，求最长子串的长度，要求其中每个字符出现次数都不少于 `k`。

## A
**一句话。** 分治：找到一个出现次数小于 `k` 的字符，按它把串切开，对每段递归。

```python
def longest_substring(s, k):
    if len(s) < k:
        return 0
    count = Counter(s)
    bad = next((c for c, v in count.items() if v < k), None)
    if bad is None:
        return len(s)                # 整串已合法
    # 含 bad 的子串一定不合法，按它切开
    parts = s.split(bad)
    return max(longest_substring(p, k) for p in parts)
```

**复杂度。** 时间 `O(26n)`，空间 `O(26 + 递归深度)`。

**易错点。**
- 删除坏字符再拼接，而不是切开：`"aaacbbb", k=3` 删 `c` 得 `6`，正确是 `3`。
- 套普通双指针：窗口合法性不单调，会漏解。

**追问。**
- 滑窗怎么做？：枚举窗口允许的字符种数 `t`，维护 `unique` 和 `enough`，相等且等于 `t` 时更新答案。
- 字符集很大怎么办？：两种解法都是 `O(nσ)`，`σ` 接近 `n` 时退化成 `O(n^2)`。

**同模式。** LC 340 至多包含 K 个不同字符的最长子串、LC 424 替换后的最长重复字符、LC 3 无重复字符的最长子串、LC 1763 最长的美好子字符串
