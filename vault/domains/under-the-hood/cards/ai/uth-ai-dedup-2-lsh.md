---
id: uth-ai-dedup-2-lsh
node: ai.dedup
type: qa
step: 2
---
## Q
**签名切段：只比同桶的**｜datatrove · 0.8.0 MinHash

每篇文章有了 112 个数的签名，仍要两两比较，怎么避免？

## A
**背景。** 签名比全文短，两两比较还是 n² 次。直觉做法：把签名切成几段，只要有一段完全相同，才值得细看；一段都不同的，几乎不可能相似。

**结构。** 局部敏感哈希（LSH，locality-sensitive hashing）的分段做法：112 个数切成 14 段，每段 8 个。每一段单独当一个键，同一段键相同的两篇文章配成一对。

**细节。**

- 真实相似度为 s 的两篇，14 段里至少一段全相同的概率是 1 − (1 − s⁸)¹⁴
- s = 0.5 时约 5%，0.7 时约 56%，0.8 时约 92%，0.9 时约 99.96%，拐点约在 0.72

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<g font-size="12" font-family="sans-serif" text-anchor="middle" fill="currentColor" stroke="currentColor">
<path d="M44 24V170H320" fill="none"/>
<polyline points="44,170 58,170 72,170 85,170 99,170 113,170 127,170 141,170 154,169 168,167 182,162 196,154 210,139 223,117 237,88 251,57 265,35 279,26 292,24 306,24 320,24" style="fill:none;stroke:var(--accent,#3b6fd4);stroke-width:2"/>
<text x="44" y="186" stroke="none">0</text>
<text x="182" y="186" stroke="none">0.5</text>
<text x="320" y="186" stroke="none">1</text>
<text x="182" y="204" style="stroke:none;fill:var(--dim,#6b7280)">两篇文章的真实相似度</text>
<text x="38" y="174" text-anchor="end" stroke="none">0%</text>
<text x="38" y="101" text-anchor="end" stroke="none">50%</text>
<text x="38" y="28" text-anchor="end" stroke="none">100%</text>
<text x="48" y="14" text-anchor="start" style="stroke:none;fill:var(--dim,#6b7280)">被配成一对的概率</text>
<circle cx="265" cy="35" r="4" style="fill:var(--accent,#3b6fd4);stroke:none"/>
<text x="256.8" y="27.2" text-anchor="end" style="stroke:none;fill:var(--accent,#3b6fd4)">0.8: 92%</text>
<text x="176" y="150.2" text-anchor="end" style="stroke:none;fill:var(--dim,#6b7280)">0.5: 5%</text>
</g>
</svg>
```

- datatrove 不建哈希表：每段的签名写成已排序的文件，合并时相邻两条签名相同，就记为一对重复

**为什么。** 一段 8 个数要全对才算，低相似度的文章几乎碰不到；但有 14 次机会，高相似度的几乎一定碰到。段更长则更严，段更多则更松。

**例题：** LC 49 字母异位词分组（同样是给每个元素算一个键，同键才进同一桶）

给一个字符串数组，把字母相同、顺序不同的词分到同一组。例：`["eat","tea","tan","ate","nat","bat"]` → `[["bat"],["nat","tan"],["ate","eat","tea"]]`。

```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        count = [0] * 26                       # 26 个字母的出现次数就是指纹
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)         # list 不可哈希，转成 tuple 才能当键
    return list(groups.values())
```
