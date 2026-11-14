---
slug: concatenated-words
---
## Q
**LC 472 连接词**｜Hard

从不重复的 `words` 中找出所有由数组里至少两个较短单词拼成的单词。

## A
**一句话。** 对每个单词做一次单词拆分（Word Break）DP，词典是全体 `words`，但不许整词算一块。

```python
def find_all_concatenated_words(words):
    ws = set(words)

    def can_split(w):
        n = len(w)
        dp = [True] + [False] * n   # dp[i]：w[:i] 能拆开
        for i in range(1, n + 1):
            for j in range(i):
                if j == 0 and i == n:
                    continue        # 整词本身不算一块
                if dp[j] and w[j:i] in ws:
                    dp[i] = True
                    break
        return dp[n]

    return [w for w in words if can_split(w)]
```

**复杂度。** 时间 `O(Σ L³)`，空间 `O(Σ L)`。

**易错点。**
- 忘了排除整词：每个词都能拆成它自己，结果变成全部 `words`。
- 把「至少两个词」当成「两个不同的词」：`["a","aa"]` 里 `"aa"` = `"a"+"a"` 也是连接词。

**追问。**
- 怎么还原拆分方式？：`dp` 同时记前驱 `prev[i] = j`，回溯。
- 要求用 Trie + DFS？：词典建前缀树，从 `i` 沿树走，遇到词尾就递归 `j + 1`，失配即停；失败的起点记进 memo，省掉切片和哈希。

**同模式。** LC 139 单词拆分、LC 140 单词拆分 II、LC 208 实现前缀树、LC 1048 最长字符串链
