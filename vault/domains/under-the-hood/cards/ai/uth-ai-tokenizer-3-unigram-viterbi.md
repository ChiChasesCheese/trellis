---
id: uth-ai-tokenizer-3-unigram-viterbi
node: ai.tokenizer
type: qa
step: 3
---
## Q
**Unigram：不枚举也能挑出最优切法**｜SentencePiece · 0.2

同一个词有好几种切法（`hugs` 可以是 `hug`+`s`，也可以是 `h`+`ug`+`s`）。SentencePiece 的 Unigram 怎样不逐个枚举，就挑出最好的一种？

## A
**背景。** BPE 的切法由合并表的先后决定，只有一个答案。Unigram 给词表里每个片段一个概率，一种切法的得分是各片段概率相乘（取对数就是相加），得分最高的胜出。切法数量随长度指数增长，不能逐个枚举。

**结构。** 动态规划（DP）：`best[i]` 是前 `i` 个字符的最优得分，等于所有以 `i` 结尾的片段里 `best[i - 片段长度] + 片段得分` 的最大值；记下来源，最后往回读出切法。这就是维特比算法（Viterbi），也是单词拆分的 DP。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 196">
<path d="M 30 82 Q 142.5 -42 255 82" style="fill:none;stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="142.5" y="15" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">hug 4</text>
<path d="M 105 82 Q 180 30 255 82" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="180" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ug 4</text>
<path d="M 30 102 Q 67.5 126 105 102" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="67.5" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h 3</text>
<path d="M 105 102 Q 142.5 126 180 102" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="142.5" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">u 3</text>
<path d="M 180 102 Q 217.5 126 255 102" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="217.5" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g 3</text>
<path d="M 255 102 Q 292.5 126 330 102" style="fill:none;stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="292.5" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">s 2</text>
<circle cx="30" cy="92" r="10" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="30" y="96.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="105" cy="92" r="10" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="105" y="96.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="180" cy="92" r="10" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="180" y="96.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="255" cy="92" r="10" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="255" y="96.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="330" cy="92" r="10" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="330" y="96.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="30" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="105" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="180" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="255" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="330" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="180" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">节点下的数字: 到这里的最小总代价</text>
</svg>
```

**细节。**

- 图里的代价是假设的，越小越好（概率取负对数）：`hug`+`s` 总代价 6，`h`+`ug`+`s` 是 9
- 位置 3 有三条路可到（`hug` 4，`ug` 3+4，`g` 6+3），只留最小的 4
- 从位置 `i` 起有哪些片段在词表里，靠字典树（trie）往下走查出

**为什么。** 同一句话的多种切法都有概率，训练时可以随机抽次优切法当数据增强；BPE 只有一种。代价：要先放很大的候选词表，再反复删掉最没用的 10%–20%。

**例题：** LC 139 单词拆分（同类：LC 140 单词拆分 II）

给字符串 `s` 和单词列表 `wordDict`，判断 `s` 能否拆成若干个字典单词。例：`s = "leetcode"`、`wordDict = ["leet","code"]` → `true`。Unigram 的 DP 多了一步：片段带分数，不只判断能不能拆，还要挑总分最高的拆法。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)                       # 哈希集合：判断"切片是不是单词"是 O(L)
    max_len = max(map(len, words))               # 单词最长 max_len，更长的切片不用试
    dp = [True] + [False] * len(s)               # dp[i]：前 i 个字符 s[:i] 能否被拆成单词
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(max(0, i - max_len), i))
    return dp[-1]
```
