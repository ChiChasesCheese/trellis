---
slug: split-two-strings-to-make-palindrome
---
## Q
**LC 1616 分割两个字符串得到回文串**｜Medium

两个等长字符串 `a`、`b`。选一个下标把两个串各切成前缀和后缀，拼成 `a前缀 + b后缀` 或 `b前缀 + a后缀`。问能否拼出回文串。

## A
**一句话。** 用 `a` 的头和 `b` 的尾向中间配对，配到第一个不相等处，剩下的中间段只要在 `a` 或 `b` 中自己是回文即可。

```python
def check_palindrome_formation(a, b):
    def pal(s, i, j):
        return s[i:j + 1] == s[i:j + 1][::-1]

    def ok(a, b):
        i, j = 0, len(a) - 1
        while i < j and a[i] == b[j]:   # 头尾配对
            i += 1
            j -= 1
        # 剩下的一段 [i, j] 由 a 或 b 整段提供
        return i >= j or pal(a, i, j) or pal(b, i, j)

    return ok(a, b) or ok(b, a)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只试 `a前缀 + b后缀`：另一个方向 `b前缀 + a后缀` 也要试。
- 剩余段只查一个串：中间段落在哪个串里都可以，`a` 或 `b` 回文就行。

**追问。**
- 为什么中间段只需看 `a` 或 `b` 自己？：切点在 `[i, j]` 内时，`a` 的头已和 `b` 的尾配完，中间只剩前缀一边的内容。

**同模式。** LC 125 验证回文串、LC 680 验证回文串 II、LC 1312 让字符串成为回文串的最少插入次数、LC 5 最长回文子串
