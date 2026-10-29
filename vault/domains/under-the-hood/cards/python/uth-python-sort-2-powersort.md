---
id: uth-python-sort-2-powersort
node: python.sort
type: qa
step: 2
---
## Q
**该先归并哪两个 run**｜Python · CPython 3.11 起

Timsort 把数据切成许多 run，什么时候合并、先合并哪两个？3.11 改了什么？

## A
**背景。** 合并两段的代价约等于它们的长度之和，所以合并的先后顺序会影响总工作量。例：长度 1000、1000、10 的三段，先合并前两段再并 10，复制 2000 + 2010 = 4010；先合并后两段再并 1000，复制 1010 + 2010 = 3020。大段尽量晚合并。

**结构。** 发现的 run 先放进一个栈里；发现新 run 时先合并栈顶相邻的 run，再入栈。3.11 起用 Powersort（Munro 与 Wild）决定合并哪两个：给每对相邻 run 的分界算一个 power，即它在一棵想象的、对半切分的二叉归并树里的深度。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<rect x="30" y="110" width="84" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="72" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="114" y="110" width="28" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="128" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="142" y="110" width="42" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="163" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="184" y="110" width="126" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="247" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<line x1="116" y1="92" x2="182" y2="92" stroke-width="1.5" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="116" y1="92" x2="116" y2="106" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="182" y1="92" x2="182" y2="106" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<text x="192" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<line x1="32" y1="74" x2="182" y2="74" stroke-width="1.5" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="32" y1="74" x2="32" y2="106" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="182" y1="74" x2="182" y2="106" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<text x="192" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<line x1="32" y1="56" x2="308" y2="56" stroke-width="1.5" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="32" y1="56" x2="32" y2="106" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="308" y1="56" x2="308" y2="106" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<text x="318" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="170" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">括号旁的编号 = 合并先后</text>
<line x1="114" y1="138" x2="114" y2="146" stroke-width="1.2" stroke="currentColor"/>
<text x="114" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="142" y1="138" x2="142" y2="146" stroke-width="1.2" stroke="currentColor"/>
<text x="142" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="184" y1="138" x2="184" y2="146" stroke-width="1.2" stroke="currentColor"/>
<text x="184" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="14" y="162" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">power</text>
<text x="170" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">power 越大 分界越深 越先合并</text>
<text x="170" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
</svg>
```

**细节。**

- 栈里 power 严格递减，深度更大的相邻 run 先合并。
- 3.10 及以前的规则基于斐波那契式的不变式；研究者做机器证明时发现它并不总成立。

**为什么。** 相当于用近似最优的二叉树决定合并顺序，对任意 run 长度分布都近似最优，规则也简单。

**例题：** LC 1167 连接木棍的最低费用

每次取两根长度为 `x`、`y` 的木棍连成一根长 `x + y` 的，代价也是 `x + y`，重复直到只剩一根，求最小总代价。

```python
import heapq

def connect_sticks(sticks: list[int]) -> int:
    heapq.heapify(sticks)
    cost = 0
    while len(sticks) > 1:
        merged = heapq.heappop(sticks) + heapq.heappop(sticks)
        cost += merged
        heapq.heappush(sticks, merged)
    return cost
```
