---
id: uth-ai-tokenizer-1-bpe-merge
node: ai.tokenizer
type: qa
step: 1
---
## Q
**BPE：文字怎样变成编号**｜tiktoken · 0.14

模型只认数字。一句话要怎样切成一串编号（token），既不太长，也不会遇到没见过的词？

## A
**背景。** 一个字母一个编号：什么字都认得，可一句话要上百个编号，太贵。一个单词一个编号：序列短，但新词、错别字没有编号，词表也越涨越大。折中：从字节出发，把老是挨在一起的片段逐步粘成新编号。

**结构。** 字节对编码（BPE，byte pair encoding）。训练：数相邻两块出现的次数，把最多的一对粘成新块，编号依次往后排，重复到词表够大；编号先后就是合并优先级（序号，rank）。编码：每轮合并序号最小的一对，直到没有可合的。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<rect x="12" y="10" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="28" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<rect x="48" y="10" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="64" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<rect x="84" y="10" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="100" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w</text>
<rect x="120" y="10" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="136" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<rect x="156" y="10" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="172" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">s</text>
<rect x="192" y="10" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="208" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t</text>
<text x="236" y="27.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">起点: 6 个字节</text>
<rect x="12" y="50" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="28" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<rect x="48" y="50" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="64" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<rect x="84" y="50" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="100" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w</text>
<rect x="120" y="50" width="68" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="154" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">es</text>
<rect x="192" y="50" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="208" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t</text>
<text x="236" y="67.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">e+s 序号 256</text>
<rect x="12" y="90" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="28" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<rect x="48" y="90" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="64" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<rect x="84" y="90" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="100" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w</text>
<rect x="120" y="90" width="104" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="172" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">est</text>
<text x="236" y="107.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">es+t 序号 257</text>
<rect x="12" y="130" width="68" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="46" y="147.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lo</text>
<rect x="84" y="130" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="100" y="147.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w</text>
<rect x="120" y="130" width="104" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="172" y="147.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">est</text>
<text x="236" y="147.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">l+o 序号 258</text>
<rect x="12" y="170" width="104" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="64" y="187.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">low</text>
<rect x="120" y="170" width="104" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="172" y="187.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">est</text>
<text x="236" y="187.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">lo+w 序号 259</text>
<text x="170" y="218" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每轮合并序号最小的相邻对</text>
</svg>
```

**细节。**

- 玩具语料里 `e`+`s` 出现 9 次，最先合并，序号 256；之后依次是 `est`、`lo`、`low`
- `lowest` 没出现过，也能切成 `low`+`est`；最坏退化成单字节，所以没有「未知词」
- GPT-2 的词表：256 个字节 + 5 万次合并 + 1 个结束符 = 50257

**为什么。** 比逐词编号多了「什么都能编」，比逐字母编号短得多；代价是生僻词会被切碎。

**例题：** LC 347 前 K 个高频元素（同类：LC 692 前 K 个高频单词）

给整数数组 `nums` 和整数 `k`，返回出现次数最多的前 `k` 个元素。例：`nums = [1,1,1,2,2,3]`、`k = 2` → `[1,2]`。BPE 训练的每一轮就是 `k = 1`：数出所有相邻对的出现次数，取最多的那一对。

```python
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]   # 下标 = 出现次数
    for x, c in count.items():
        buckets[c].append(x)
    ans: list[int] = []
    for bucket in reversed(buckets):          # 从高频到低频
        ans.extend(bucket)
        if len(ans) >= k:
            return ans[:k]
    return ans
```
