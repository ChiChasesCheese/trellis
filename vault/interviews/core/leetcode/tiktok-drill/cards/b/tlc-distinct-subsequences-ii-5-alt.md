---
id: tlc-distinct-subsequences-ii-5-alt
node: b.distinct-subsequences-ii
type: qa
step: 5
---
## Q
**LC 940 不同的子序列 II**｜Hard · 字节高频｜另一种解法

除了「`dp[i]` + 上次出现位置」，还有什么做法？按末尾字符分类怎么写？和暴力的集合法比，各适合什么规模？

## A
**按末尾字符分类。** `end[c]` 是以字母 `c` 结尾的不同子序列个数。读到 `ch`：所有已有的不同子序列（含空串）后面接上 `ch`，得到以 `ch` 结尾的全部串，共 `sum(end) + 1` 个；旧的 `end[ch]` 是它的子集，所以直接**覆盖**而不是累加。

```python
def distinct_subseq_ii_alt(s: str) -> int:
    MOD = 10 ** 9 + 7
    end = [0] * 26                  # end[c]：以字母 c 结尾的不同子序列个数
    for ch in s:
        c = ord(ch) - ord("a")
        end[c] = (sum(end) + 1) % MOD     # 所有旧子序列（含空串）后面接 ch，整体替换旧值
    return sum(end) % MOD
```

`"abc"` → `7`，`"aba"` → `6`，`"aaa"` → `3`，`"abcdefghijklmnopqrstuvwxyz" * 76` → `238585536`，与主解一致。

**暴力集合法。** 枚举 `2^n` 个选法，用 `set` 去重，只在 `n <= 20` 时可行，适合当小数据的参照。

**怎么选。** 要讲清楚「为什么重复数是 `dp[j - 1]`」，用主解；字符集小、要省内存、要处理字符流，用 `end` 数组，空间 `O(26)`，没有减法也就没有负数；`n <= 20` 想快速自查，用集合法。
