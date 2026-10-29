---
id: uth-gaps-dp-join-order-1-levels
node: gaps.dp-join-order
type: qa
step: 1
---
## Q
**多张表连接，先连谁后连谁**｜PostgreSQL · 17

`FROM t1, t2, t3, t4` 四张表要连成一张结果，先连哪两张，后面中间结果的大小能差几个数量级。规划器怎样找到最便宜的连接顺序？

## A
**背景。** 连接（join）一次只能拼两张表，多张表要一步步拼，每步产生一张中间表。先拼小表，中间表小，后面的活轻；先拼大表，后面全被拖慢。最笨的办法是把所有顺序都估一遍成本：直线式的拼法就有 n! 种，12 张表是 4.79 亿种。而且很多顺序前半段完全一样，却各算了一遍。

**结构。** 动态规划（dynamic programming）：按「已拼进几张表」一层层往上，每个「表的集合」只记下最便宜的拼法，高一层直接用。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<line x1="80" y1="158" x2="115" y2="134" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="150" y1="158" x2="115" y2="134" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="150" y1="158" x2="185" y2="134" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="220" y1="158" x2="185" y2="134" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="220" y1="158" x2="255" y2="134" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="290" y1="158" x2="255" y2="134" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="115" y1="110" x2="150" y2="86" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="185" y1="110" x2="150" y2="86" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="185" y1="110" x2="220" y2="86" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="255" y1="110" x2="220" y2="86" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="150" y1="62" x2="185" y2="38" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="220" y1="62" x2="185" y2="38" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="30" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">4 张</text>
<text x="8" y="78" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">3 张</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">2 张</text>
<text x="8" y="174" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">1 张</text>
<rect x="52" y="158" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">t1</text>
<rect x="122" y="158" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">t2</text>
<rect x="192" y="158" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">t3</text>
<rect x="262" y="158" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">t4</text>
<rect x="83" y="110" width="64" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="115" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1 2</text>
<rect x="153" y="110" width="64" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="185" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2 3</text>
<rect x="223" y="110" width="64" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="255" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3 4</text>
<rect x="118" y="62" width="64" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="150" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1 2 3</text>
<rect x="188" y="62" width="64" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="220" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2 3 4</text>
<rect x="141" y="14" width="88" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="185" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1 2 3 4</text>
<text x="170" y="206" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">每个集合只记下最便宜的拼法 更高层直接用</text>
</svg>
```

**细节。**

- 图里的条件是 `t1=t2, t2=t3, t3=t4`：没有条件相连的组合（如 `{1 3}`）根本不生成
- 同一个集合不管怎么拼出来，共用一条记录，各种拼法在里面比成本

**为什么。** 重复的前半段只算一次；代价是集合数仍随表数指数增长，表很多时要换算法。

**例题：** LC 691 贴纸拼词（同类：LC 698 划分为k个相等的子集）

有 `n` 种贴纸，每张上是一个小写单词，每种数量无限。从贴纸上剪下单个字母、可任意重排，拼出字符串 `target`，返回最少需要的贴纸数，做不到返回 `-1`。`1 <= n <= 50`，`1 <= target.length <= 15`。

```python
from collections import Counter, defaultdict
from math import inf


def min_stickers(stickers: list[str], target: str) -> int:
    n = len(target)
    full = (1 << n) - 1
    has_letter: defaultdict[str, list[Counter[str]]] = defaultdict(list)
    for s in stickers:
        cnt = Counter(s)
        for ch in cnt:
            has_letter[ch].append(cnt)          # 按字母索引：含该字母的贴纸

    dp = [inf] * (1 << n)                       # dp[mask]：凑出 target 中 mask 这些位置所需的最少贴纸
    dp[0] = 0
    for mask in range(full):
        if dp[mask] == inf:
            continue
        low = (~mask & (mask + 1)).bit_length() - 1      # 最低的未覆盖位置
        for cnt in has_letter[target[low]]:              # 只试能盖住它的贴纸
            left, new = cnt.copy(), mask
            for i, ch in enumerate(target):              # 贴纸字母能盖多少盖多少
                if not new >> i & 1 and left[ch] > 0:
                    left[ch] -= 1
                    new |= 1 << i
            dp[new] = min(dp[new], dp[mask] + 1)
    return -1 if dp[full] == inf else dp[full]
```
