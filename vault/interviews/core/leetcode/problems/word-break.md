---
slug: word-break
---
## Q
**LC 139 单词拆分**｜Medium

判断字符串 `s` 能否拆成若干字典单词（可重复使用）。

## A
**一句话。** 前缀 DP：`dp[i]` 为真当且仅当存在 `j` 使 `dp[j]` 为真且 `s[j:i]` 在字典里。

```python
def word_break(s, word_dict):
    words = set(word_dict)        # 集合查找
    max_len = max(map(len, words))
    dp = [True] + [False] * len(s)    # dp[i]：s[:i] 可拆
    for i in range(1, len(s) + 1):
        lo = max(0, i - max_len)      # 切点只看最近 max_len 位
        dp[i] = any(dp[j] and s[j:i] in words
                    for j in range(lo, i))
    return dp[-1]
```

**复杂度。** 时间 `O(n·L²)`（`L` 为最长单词），空间 `O(n)`。

**易错点。**
- `dp[0]` 不设 `True`：整张表全 `False`。
- 字典用 `list` 查找：每次 `O(|dict|)`，先转 `set`。
- 贪心遇词就切：`"aaaaaaa"`、`["aaaa","aaa"]` 先切 `aaa` 会失败，应为 `True`。

**追问。**
- 返回所有拆分（LC 140）？：从 0 起 DFS，`@cache` 记每个起点的后缀方案，方案数可能指数级。
- 字典很大或单词很长？：建 Trie，从每个起点沿 `s` 往下走，走不通就停。

**同模式。** LC 140 单词拆分 II、LC 91 解码方法、LC 279 完全平方数、LC 322 零钱兑换
