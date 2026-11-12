---
slug: longest-string-chain
---
## Q
**LC 1048 最长字符串链**｜Medium

单词 A 插入恰好一个字母（任意位置）得到 B，则 A 是 B 的前身。求 `words` 中最长的前身链长度。

## A
**一句话。** 按长度升序处理，`dp[w]` 是 `1 +` 删去任一字母后的串的 `dp` 最大值。

```python
def longest_str_chain(words):
    dp = {}              # dp[w]：以 w 结尾的最长链
    for w in sorted(words, key=len):
        best = 0
        for i in range(len(w)):
            best = max(best, dp.get(w[:i] + w[i+1:], 0))
        dp[w] = best + 1
    return max(dp.values())
```

**复杂度。** 时间 `O(N·L²)`，空间 `O(N·L)`。

**易错点。**
- 不按长度排序：前身还没算，`["bdca","bda","bca","ba","a"]` 得 `1`，应为 `4`。
- 只比较字母多重集、忽略顺序：`"ab"` 和 `"bca"` 会被当成前身。
- 直接 `dp[候选]`：候选不在表里会 `KeyError`，要 `get(..., 0)`。

**追问。**
- 怎么还原具体的链？：另存 `prev[w]`，从最大值的词沿它回溯。
- 前身改成「替换一个字母」？：长度不再递增，没有天然的处理顺序，改用图搜索。

**同模式。** LC 300 最长递增子序列、LC 354 俄罗斯套娃信封问题、LC 368 最大整除子集、LC 127 单词接龙
