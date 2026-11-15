---
slug: maximum-score-words-formed-by-letters
---
## Q
**LC 1255 得分最高的单词集合**｜Hard

给单词列表 `words`、可用字母列表 `letters`（每个字母只能用它出现的次数）和 26 个字母的分数 `score`。每个单词至多选一次，选的单词用掉相应字母，求能得到的最大总分。

## A
**一句话。** 对每个单词做「选或不选」的回溯：字母够就扣掉并加分，递归后还原。

```python
def max_score_words(words, letters, score):
    cnt = Counter(letters)
    def dfs(i):
        if i == len(words):
            return 0
        best = dfs(i + 1)                  # 不选 words[i]
        need = Counter(words[i])
        if all(cnt[c] >= k for c, k in need.items()):
            for c, k in need.items():
                cnt[c] -= k                # 选：扣掉字母
            gain = sum(score[ord(c) - 97] for c in words[i])
            best = max(best, gain + dfs(i + 1))
            for c, k in need.items():
                cnt[c] += k                # 回溯：还原
        return best
    return dfs(0)
```

**复杂度。** 时间 `O(2^n · L)`，空间 `O(n)`。

**易错点。**
- 回溯后忘了还原字母计数：之后的分支看到的库存是错的。
- 同一个单词选多次：每个单词至多选一次，选或不选就推进到下一个下标。
- 先用单词里字母的分数排序贪心：局部高分的词可能挤占字母，要枚举子集。

**追问。**
- 还有更快的写法吗？：枚举子集的位掩码，用子集累加字母数检查，常数差不多。
- 为什么 `n ≤ 14` 能暴力？：`2^14` 种子集，每种代价 `O(L)`。

**同模式。** LC 78 子集、LC 1239 串联字符串的最大长度、LC 2002 两个回文子序列长度的最大乘积
