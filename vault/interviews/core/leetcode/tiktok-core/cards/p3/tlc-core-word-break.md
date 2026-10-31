---
id: tlc-core-word-break
node: p3.word-break
type: qa
---
## Q
**LC 139 单词拆分**｜Medium · LC TikTok 全时段热度 56/100 · 近一年被问：美国 2 次、国内 0 次 · CodeTop 国内累计 44 次 · 最近 2026-08-27（国内 CodeTop） · 也在：Amazon、LeetCode Hot 100、Blind 75、NeetCode 150、Top Interview 150

给字符串 `s` 和字符串列表 `wordDict`（字典）。如果能用字典里的一个或多个单词拼接出 `s` 就返回 `true`；单词可以重复使用，也不要求用完字典。`1 <= s.length <= 300`，`1 <= wordDict.length <= 1000`，`1 <= wordDict[i].length <= 20`，`s` 和单词都只含小写字母，字典里的单词互不相同。例：`s = "leetcode", wordDict = ["leet","code"]` → `true`；`s = "applepenapple", wordDict = ["apple","pen"]` → `true`（单词可复用）；`s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** `dp[i]` 表示前缀 `s[:i]` 能否被拆成字典单词；`dp[i]` 为真，当且仅当存在 `j < i` 使得 `dp[j]` 为真且 `s[j:i]` 在字典里，`j` 只需在 `[i - 最长单词长度, i)` 里枚举。`O(n · L)` 次切片查找（`L` 是最长单词长度）。

**识别。** 「能否把序列切成若干合法片段」是线性序列上的 DP 信号：前缀能否拆分只取决于更短前缀的结果。朴素递归会从同一个位置反复出发，说明子问题重叠，值得记忆。`n <= 300`、单词长 `<= 20`，`O(n·L)` 次查找绰绰有余。

**推导。** 暴力：递归尝试每个能匹配的前缀单词，失败回溯，最坏指数级（`"aaaa…ab"` 配 `"a"`、`"aa"`、`"aaa"`）。浪费：「从位置 `i` 往后能不能拆成功」只和 `i` 有关，却被不同的前缀组合反复重算。洞察：自底向上，`dp[0] = True`（空前缀），逐个位置往前找一个合法的切点；单词最长 `L`，切点只需看最近 `L` 个位置；把字典放进 `set`，切片查找 `O(L)`。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)                       # 哈希集合：判断"切片是不是单词"是 O(L)
    max_len = max(map(len, words))               # 单词最长 max_len，更长的切片不用试
    dp = [True] + [False] * len(s)               # dp[i]：前 i 个字符 s[:i] 能否被拆成单词
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(max(0, i - max_len), i))
    return dp[-1]
```

**运行。** 例 1 → `True`；例 2 → `True`；例 3 → `False`；`("a", ["b"])` → `False`；`("aaaaaaa", ["aaaa", "aaa"])` → `True`；`("a" * 299 + "b", ["a", "aa", …, "a" * 20])` → `False`（瞬间返回）。

**复杂度。** 时间 `O(n · L²)`：`n` 个位置，每个最多试 `L` 个切点，每次切片加哈希 `O(L)`，约 `300 · 20 · 20 = 1.2 * 10^5`；空间 `O(n + 字典总长度)`。

**易错点。**
- `dp[0]` 必须是 `True`（空前缀可拆），否则整张表全是 `False`。
- 字典用 `list` 查找 `s[j:i] in word_dict` 是 `O(|dict|)`，会把复杂度乘上 1000；先转成 `set`。
- 贪心地"遇到单词就切"是错的：`s = "aaaaaaa", wordDict = ["aaaa","aaa"]`，遇到 `"aaa"` 就切会得到 `"aaa" + "aaa"` 剩下一个 `a`，返回 `False`，正确答案是 `True`（`"aaaa" + "aaa"`）。

**追问。**
- 返回所有拆分方案（LC 140）：从位置 0 做 DFS，用 `@cache` 记忆每个起点的后缀方案；方案数可能指数级，要说明输出规模。
- 字典很大或单词很长：建 Trie，从每个起点沿 `s` 往下走，走不下去就停，省掉切片和哈希。
- 返回一种具体拆法或最少单词数：`dp` 改存最少单词数，并记录前驱 `prev[i]` 回溯。

**同模式。** LC 140 单词拆分 II、LC 91 解码方法、LC 279 完全平方数、LC 322 零钱兑换、LC 472 连接词。
