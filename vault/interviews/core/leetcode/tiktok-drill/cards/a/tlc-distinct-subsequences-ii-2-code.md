---
id: tlc-distinct-subsequences-ii-2-code
node: a.distinct-subsequences-ii
type: qa
step: 2
---
## Q
**LC 940 不同的子序列 II**｜Hard · 字节高频｜写出 Python 实现

小写字母串 `s`（`1 <= s.length <= 2000`），求它的不同非空子序列个数，对 `10^9 + 7` 取余。用一维 DP 加一个「字符上次出现位置」的字典。

## A
**思路。** `dp[i]` 为 `s[:i]` 的不同子序列数，含空串，`dp[0] = 1`。读到第 `i` 个字符：先翻倍；若该字符以前出现过，减去 `dp[上次位置 - 1]`；再记下这次位置。答案是 `dp[n] - 1`。

```python
def distinct_subseq_ii(s: str) -> int:
    MOD = 10 ** 9 + 7
    n = len(s)
    dp = [1] * (n + 1)              # dp[i]：s[:i] 的不同子序列个数，含空串
    last: dict[str, int] = {}       # 字符 -> 它上一次出现的位置（从 1 开始）
    for i, ch in enumerate(s, 1):
        dp[i] = 2 * dp[i - 1] % MOD                 # 每个旧子序列：不接 ch / 接 ch
        if ch in last:                              # 接 ch 得到的串里，有一批在上次已经造过
            dp[i] = (dp[i] - dp[last[ch] - 1]) % MOD
        last[ch] = i
    return (dp[n] - 1) % MOD        # 去掉空串
```

运行：`"abc"` → `7`，`"aba"` → `6`，`"aaa"` → `3`，`"a"` → `1`，`"a" * 2000` → `2000`，`"abcdefghijklmnopqrstuvwxyz" * 76` → `238585536`。

**复杂度。** 时间 `O(n)`：一次扫描，每步常数；空间 `O(n)`：`dp` 数组，字典最多 26 项。

**写法要点。** `enumerate(s, 1)` 让位置从 `1` 开始，与 `dp[i]` 的含义对齐；`ch in last` 判断是否出现过，再取 `last[ch]`；`dp = [1] * (n + 1)` 先全部填 `1`，`dp[0] = 1` 就是空串；`% MOD` 放在每次减法之后，Python 的取模保证非负；`MOD = 10 ** 9 + 7` 写成表达式，比写 `1000000007` 不易数错零。
