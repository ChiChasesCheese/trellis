---
id: tlc-word-break-3-why
node: p3.word-break
type: qa
step: 3
---
## Q
**LC 139 单词拆分**｜正确性

为什么 `dp[i]` 只需要看「存在一个切点 `j`，使 `dp[j]` 为真且 `s[j:i]` 是单词」？为什么只枚举最近 `max_len` 个切点就够？

## A
**不变量。** `dp[i]` 为真，当且仅当 `s[:i]` 存在一种拆分。任何拆分的最后一个单词是某个 `s[j:i]`，它之前的部分 `s[:j]` 本身也被拆成单词，所以 `dp[j]` 为真；反过来，`dp[j]` 为真且 `s[j:i]` 是单词，就能拼出 `s[:i]` 的一种拆分。最后一个单词长度不超过 `max_len`，因此 `j >= i - max_len`，更远的切点不可能。`dp[0] = True` 是递推的起点。

**反例（错误写法一）：贪心地遇到单词就切。** `s = "aaaaaaa", wordDict = ["aaaa","aaa"]`：从左边逐字符累积，遇到 `"aaa"` 就切，切两次后剩一个 `a` 匹配不上，返回 `False`；正确答案是 `True`（`"aaaa" + "aaa"`）。

**反例（错误写法二）：`dp[0]` 写成 `False`。** 任何位置的递推都依赖空前缀，整张表全是 `False`，`("leetcode", ["leet","code"])` 会返回 `False`，正确是 `True`。
