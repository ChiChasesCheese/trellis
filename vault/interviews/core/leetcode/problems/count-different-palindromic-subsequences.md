---
slug: count-different-palindromic-subsequences
---
## Q
**LC 730 统计不同回文子序列**｜Hard

字符串 `s` 只含 `a`、`b`、`c`、`d`。返回 `s` 中不同的非空回文子序列个数，对 `10^9 + 7` 取模（内容不同才算不同）。

## A
**一句话。** 对区间 `[i, j]` 枚举最外层字符 `c`：取 `c` 在区间内第一次和最后一次出现的位置，这样每种内容只数一次，`c` 本身、`cc` 以及 `c + 内层回文 + c` 都由此算出。

```python
def count_pal_subseq(s):
    MOD = 10 ** 9 + 7
    pos = {c: [i for i, x in enumerate(s) if x == c]
           for c in "abcd"}
    @cache
    def f(i, j):                 # s[i..j] 里不同的回文子序列
        total = 0
        for c in "abcd":
            p = pos[c]
            a = bisect_left(p, i)
            b = bisect_right(p, j) - 1
            if a > b:
                continue         # 区间里没有 c
            total += 1           # 单个 c
            if b > a:            # 两端都取到 c
                total += 1 + f(p[a] + 1, p[b] - 1)
        return total % MOD
    return f(0, len(s) - 1)
```

**复杂度。** 状态 `O(n^2)`，每个状态 `O(log n)`，时间 `O(n^2 log n)`，空间 `O(n^2)`。

**易错点。**
- 取任意一对 `c` 而不是最外层的一对：同样的内容被重复计数。
- 漏掉 `cc`：当 `a < b` 时 `c + c`（内层为空）单独算 1 个，`c + X + c` 的 `X` 必须非空。
- 区间为空时不返回 0：`i > j` 时区间里没有任何字符，`a > b` 已覆盖。

**追问。**
- 为什么用「最外层 `c`」就不会重复？：任何回文子序列的两端字符固定后，取最靠外的一对位置能得到最大的内层区间，内层的所有可能都被包含，且不同内容互不重叠。
- 字母表更大怎么办？：每个状态枚举全部字母，复杂度乘以字母表大小。

**同模式。** LC 516 最长回文子序列、LC 940 不同的子序列 II、LC 647 回文子串、LC 115 不同的子序列
