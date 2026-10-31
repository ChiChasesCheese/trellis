---
id: tlc-concatenated-words-0-whole
node: c.concatenated-words
type: qa
---
## Q
**LC 472 连接词**｜Hard · LC TikTok 全时段热度 25/100 · CodeTop 国内累计 1 次 · 最近 2022-01-01（国内 CodeTop）

给定不含重复单词的字符串数组 `words`，找出并返回 `words` 中所有的连接词。连接词是指完全由给定数组中的至少两个较短单词（不一定是不同的两个）组成的字符串。`1 <= words.length <= 10^4`，`1 <= words[i].length <= 30`，`words[i]` 仅由小写字母组成，`words` 中所有字符串唯一，`1 <= sum(words[i].length) <= 10^5`。例：`words = ["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"]` → `["catsdogcats","dogcatsdog","ratcatdogcat"]`；`words = ["cat","dog","catdog"]` → `["catdog"]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 对每个单词做一次「单词拆分」（Word Break）动态规划，词典是全体 `words`，唯一的限制是不能把单词整个当作一块。

**识别。** 「一个字符串能否拆成词典里的若干词」是 Word Break（LC 139）；连接词多了"至少两个"的要求，即拆分里不允许出现"整个单词本身"这一块。单词长度最多 30，每个单词的拆分是 `O(L²)` 个子串查询。

**推导。** 暴力递归每个前缀、递归剩余，无记忆化会指数级。`dp[i]` 表示 `word[:i]` 能否拆成词典里的若干词；`dp[0] = True`。转移：`dp[i] = any(dp[j] and word[j:i] in word_set)`。要排除"整个单词作为唯一一块"，也就是 `j = 0` 且 `i = len(word)` 这一对不允许。

```python
def find_all_concatenated_words(words: list[str]) -> list[str]:
    word_set = set(words)

    def can_split(word: str) -> bool:
        n = len(word)
        dp = [False] * (n + 1)                   # dp[i]：word[:i] 能否拆成词典里的若干词
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if j == 0 and i == n:            # 整个单词本身不算一块：至少要两块
                    continue
                if dp[j] and word[j:i] in word_set:
                    dp[i] = True
                    break
        return dp[n]

    return [w for w in words if can_split(w)]
```

运行：示例 1 → `["catsdogcats","dogcatsdog","ratcatdogcat"]`，示例 2 → `["catdog"]`；`["a","aa","aaa"]` → `["aa","aaa"]`；`["a"]` → `[]`。

**复杂度。** 时间 `O(Σ L³)`（每个单词 `L²` 个子串，每次切片和哈希 `O(L)`），`L ≤ 30` 时约 `10^5 × 900` 的量级，足够；空间 `O(Σ L)`。

**拓展优化。**
- 按长度排序，只把已处理的更短单词放进集合：拆分时用到的块一定不长于当前单词，且不可能是单词自身，因此不需要 `j == 0 and i == n` 的特判，对前缀树版本也更自然。

```python
def find_all_concatenated_words_sorted(words: list[str]) -> list[str]:
    seen: set[str] = set()                       # 只含已经处理过的（不长于当前的）单词
    ans: list[str] = []
    for word in sorted(words, key=len):
        n = len(word)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            dp[i] = any(dp[j] and word[j:i] in seen for j in range(i))
        if n and dp[n]:
            ans.append(word)
        seen.add(word)
    return ans
```

- 用前缀树代替切片加哈希，可以在走不通时立刻剪枝，常数更好。

**易错点。**
- 忘了排除"整个单词"：每个单词都能被拆成它自己，结果变成 `words` 全部。
- 把"至少两个词"理解成"至少两个不同的词"：`"aa"` 由 `"a" + "a"` 组成同样是连接词，示例 `["a","aa"]` 应返回 `["aa"]`。

**追问。**
- 返回具体的拆分方式：`dp` 同时记录前驱 `prev[i] = j`，回溯得到。
- 词典与待查单词是两个集合（LC 139 的多次查询版）：词典建一次前缀树，每个查询单词独立 DP。

**同模式。** LC 139 单词拆分、LC 140 单词拆分 II、LC 208 实现前缀树、LC 1048 最长字符串链、LC 1639 通过给定词典构造目标字符串的方案数。
