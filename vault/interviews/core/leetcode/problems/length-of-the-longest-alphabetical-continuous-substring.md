---
slug: length-of-the-longest-alphabetical-continuous-substring
---
## Q
**LC 2414 最长的字母序连续子字符串的长度**｜Medium

求小写字母串 `s` 中最长的、由字母表中连续字母组成的子串（如 `"abc"`，`"acb"`、`"za"` 不算）的长度。

## A
**一句话。** 一趟扫描维护以当前字符结尾的连续长度 `run`，恰好比前一个大 `1` 就加一，否则重置为 `1`。

```python
def longest_continuous_substring(s):
    best = run = 1             # 单个字符长度为 1
    for prev, cur in pairwise(s):
        run = run + 1 if ord(cur) - ord(prev) == 1 else 1
        best = max(best, run)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 把「差为 `1`」写成「递增」：`"acd"` 得 `3`，应为 `2`，`a` 和 `c` 之间隔了 `b`。
- 初值写成 `0`：`"a"` 返回 `0`，应为 `1`。

**追问。**
- 允许 `z` 后接 `a` 呢？：判断改成 `(ord(cur) - ord(prev)) % 26 == 1`，首尾相接的环形情形另外处理。
- 要返回子串本身？：记最长段的结束下标，切 `s[end-best+1:end+1]`。

**同模式。** LC 674 最长连续递增序列、LC 485 最大连续 1 的个数、LC 1446 连续字符、LC 978 最长湍流子数组
