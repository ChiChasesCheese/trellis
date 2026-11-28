---
id: lct-learn-greedy-4-3
node: greedy.4.3
type: qa
step: 1
---
## Q
**贪心算法 › 数学贪心 › 排序不等式**｜学习卡

套路是什么？

## A
**一句话。** 排序不等式：两组数配对相乘求和，大配大的和最大，大配小的和最小；这里把天数当一组、价值当另一组，越贵越晚买。

下图：LC 2931，两组数配对相乘，按同样顺序排好再一一配。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<text x="14" y="38" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">天数</text>
<rect x="70" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="120" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="170" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="195.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="220" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="14" y="108" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">价值升序</text>
<rect x="70" y="90" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="95.0" y="108.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="120" y="90" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="145.0" y="108.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="170" y="90" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="195.0" y="108.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="220" y="90" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="245.0" y="108.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">8</text>
<line x1="95.0" y1="48" x2="95.0" y2="88" stroke-width="1.2" stroke="currentColor"/>
<line x1="145.0" y1="48" x2="145.0" y2="88" stroke-width="1.2" stroke="currentColor"/>
<line x1="195.0" y1="48" x2="195.0" y2="88" stroke-width="1.2" stroke="currentColor"/>
<line x1="245.0" y1="48" x2="245.0" y2="88" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="290" y="64" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">大配大</text>
<text x="170" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">Σ d·v 最大：越贵越晚买</text>
</svg>

```python
def max_spending(values):
    items = sorted(v for row in values for v in row)
    # 第 d 天买第 d 小的：越贵越晚买，且顺序总是合法
    return sum(d * v for d, v in enumerate(items, 1))
```

**要点。**
- 为什么对？：顺序和 >= 乱序和 >= 逆序和：把乘数 `1..m*n` 与价值同向配对，总和最大。
- 为什么升序总是合法？：每个商店里右边的更便宜，全体升序天然先买到右边的。
- 要最小开销怎么改？：降序不合法（只能先买最右边的），要在合法顺序里取最小，是另一道题。

**易错点。**
- 排序方向写反：贵的先买，示例 1 得 `165`，应为 `285`。
- 天数从 `0` 数起：第一天乘数是 `1`，`enumerate` 要从 `1` 开始。

**对应题目。** LC 2931 购买物品的最大开销
