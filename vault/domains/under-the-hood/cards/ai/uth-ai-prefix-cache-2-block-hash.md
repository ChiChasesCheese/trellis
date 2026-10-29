---
id: uth-ai-prefix-cache-2-block-hash
node: ai.prefix-cache
type: qa
step: 2
---
## Q
**用链式哈希找已算过的块**｜vLLM · 自动前缀缓存

vLLM 的 KV 缓存按固定大小的块存放，没有树。新请求来了，它怎样知道哪些块已经算过？

## A
**背景。** 块（默认 16 个 token）是现成的单位，想用哈希表按内容查块。键只用这一块的 token 不行：同样的 16 个 token 放在不同的前文后面，KV 并不相同，键必须包含整个前文。

**结构。** 链式哈希：块 `i` 的哈希 = hash(块 `i-1` 的哈希，本块 token，额外信息)，每个哈希都「指纹」了从开头到这一块的全部内容。只给装满的块算，哈希表把哈希映射到物理块。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="12" y="40" width="64" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="44" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块0</text>
<text x="44" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">h0</text>
<line x1="44" y1="80" x2="44" y2="86" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="44,86 41,79 47,79" style="fill:var(--accent,#3b6fd4)"/>
<line x1="76" y1="57" x2="96" y2="57" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="96,57 89,60 89,54" style="fill:var(--accent,#3b6fd4)"/>
<rect x="96" y="40" width="64" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="128" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块1</text>
<text x="128" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">h1</text>
<line x1="128" y1="80" x2="128" y2="86" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="128,86 125,79 131,79" style="fill:var(--accent,#3b6fd4)"/>
<line x1="160" y1="57" x2="180" y2="57" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="180,57 173,60 173,54" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="40" width="64" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="212" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块2</text>
<text x="212" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">h2</text>
<line x1="212" y1="80" x2="212" y2="86" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="212,86 209,79 215,79" style="fill:var(--accent,#3b6fd4)"/>
<line x1="244" y1="57" x2="264" y2="57" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="264,57 257,60 257,54" style="fill:var(--accent,#3b6fd4)"/>
<rect x="264" y="40" width="64" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="296" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块3</text>
<text x="296" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没存过</text>
<text x="12" y="22" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每块 16 个 token, 只给装满的块算哈希</text>
<text x="170" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h1 = 哈希(h0, 块1 的 token)</text>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h2 = 哈希(h1, 块2 的 token)</text>
<text x="170" y="178" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前三块查表命中, 第四块起重新算</text>
</svg>
```

**细节。**

- 查找：依次查新请求每一块的哈希，第一个没命中就停，后面不可能命中
- 整个 prompt 都命中，也要重算最后一个 token（要靠它的输出生成下一个字），命中长度最多是长度减 1
- 额外信息含 LoRA 与多模态输入，避免不同适配器误用缓存
- v0.32 默认开启，哈希算法默认 `sha256`

**为什么。** 不用维护树，一次哈希查询就中；代价是只能以整块为单位命中，末尾不满一块的 token 要重算。

**例题：** LC 3043 最长公共前缀的长度

给两个正整数数组 `arr1`、`arr2`，数的前缀是它最左边的几位，求 `arr1` 与 `arr2` 的数对之间最长公共前缀的位数。例：`arr1 = [1,10,100]`、`arr2 = [1000]` → `3`。做法是把一边所有前缀放进集合，另一边从长到短查，和「按前缀指纹查表」一样。

```python
def longest_common_prefix(arr1: list[int], arr2: list[int]) -> int:
    prefixes: set[int] = set()
    for x in arr1:
        while x and x not in prefixes:     # 已经在集合里说明它的更短前缀也都在，可以提前停
            prefixes.add(x)
            x //= 10                       # 去掉最后一位 = 取前一个前缀
    best = 0
    for y in arr2:
        while y and y not in prefixes:     # 从最长的前缀往短处找第一个命中的
            y //= 10
        if y:
            best = max(best, len(str(y)))
    return best
```
