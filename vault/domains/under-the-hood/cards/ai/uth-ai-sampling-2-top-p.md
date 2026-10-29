---
id: uth-ai-sampling-2-top-p
node: ai.sampling
type: qa
step: 2
---
## Q
**top-k 与 top-p：砍掉尾巴再抽**｜transformers · 5.21

词表里有十几万个词，尾部的词概率都极小，抽到一个就会胡说八道。top-k 和 top-p 各怎样砍掉尾巴，差别在哪？

## A
**背景。** 尾巴上每个词的概率很小，但词太多，加起来的概率并不小，抽签时总有机会抽到离谱的词。办法：抽签之前，先把尾巴整个作废。

**结构。** top-k：只保留分数最高的 `k` 个词。top-p（又叫核采样，nucleus sampling）：把词按概率从大到小排好，一个个累加概率，加到总和达到 `p` 就停，留下已经加进去的词。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="34" y="28" width="34" height="76" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="51" y="23" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0.50</text>
<text x="51" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.50</text>
<rect x="80" y="66" width="34" height="38" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="97" y="61" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0.25</text>
<text x="97" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.75</text>
<rect x="126" y="85.8" width="34" height="18.2" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="143" y="80.8" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0.12</text>
<text x="143" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.87</text>
<rect x="172" y="91.8" width="34" height="12.2" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="189" y="86.8" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0.08</text>
<text x="189" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.95</text>
<rect x="218" y="99.4" width="34" height="4.6" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="235" y="94.4" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0.03</text>
<text x="235" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.98</text>
<rect x="264" y="101" width="34" height="3" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="281" y="96" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0.02</text>
<text x="281" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1.00</text>
<line x1="20" y1="104" x2="322" y2="104" stroke="currentColor" stroke-width="1"/>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下排数字: 从大到小累加的概率</text>
<line x1="34" y1="172" x2="160" y2="172" stroke="currentColor" stroke-width="2"/>
<line x1="34" y1="168" x2="34" y2="172" stroke="currentColor" stroke-width="1"/>
<line x1="160" y1="168" x2="160" y2="172" stroke="currentColor" stroke-width="1"/>
<text x="34" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">top-k=3: 留前 3 个</text>
<line x1="34" y1="202" x2="206" y2="202" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="34" y1="198" x2="34" y2="202" stroke="currentColor" stroke-width="1"/>
<line x1="206" y1="198" x2="206" y2="202" stroke="currentColor" stroke-width="1"/>
<text x="34" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">top-p=0.9: 累加到 0.95 才够, 留前 4 个</text>
</svg>
```

**细节。**

- 图中 `k=3` 留前 3 个；`p=0.9` 要累加到 0.95 才够，留前 4 个
- 模型很确定（一个词占 95%）时 top-p 只留 1 个，很犹豫时自动多留；`k` 是固定个数，做不到
- 落选词的分数被置成负无穷，softmax 后概率为 0；至少保留 1 个词
- 常见取值：top-k 取 5–50，top-p 取 0.9–0.95

**坑。** top-p 的累加包含「越线」的那个词：图中加到 0.87 还不够，要把 0.08 也算进去，才到 0.95。

**例题：** LC 1833 雪糕的最大数量

`costs[i]` 是第 `i` 支雪糕的价格，手里有 `coins` 块钱，最多能买几支？先按价格从低到高排，从头一支支累加花费，钱不够就停。top-p 是同一个骨架：按概率从高到低排，从头累加，达到 `p` 就停。

```python
def max_ice_cream(costs: list[int], coins: int) -> int:
    max_cost = max(costs)
    buckets = [0] * (max_cost + 1)  # 计数排序：下标是价格
    for cost in costs:
        buckets[cost] += 1
    count = 0
    for price in range(1, max_cost + 1):
        if buckets[price] == 0:
            continue
        take = min(buckets[price], coins // price)
        count += take
        coins -= take * price
        if coins == 0:
            break
    return count
```
