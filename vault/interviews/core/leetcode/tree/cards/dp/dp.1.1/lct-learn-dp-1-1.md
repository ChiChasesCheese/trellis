---
id: lct-learn-dp-1-1
node: dp.1.1
type: qa
step: 1
---
## Q
**动态规划 › 入门 DP › 爬楼梯**｜学习卡

套路是什么？

## A
**一句话。** 最后一步有固定的几种来源，`f[i]` 就由 `f[i - 步长]` 汇总：计数用求和，最小花费用取小再加代价。

下图：最后一步迈 1 阶或 2 阶，`f[i]` 只由这两个来源汇总。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="30" y="50" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="50.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="70" y="50" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="110" y="50" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="150" y="50" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="190" y="50" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="210.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="230" y="50" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="250.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">8</text>
<rect x="270" y="50" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">13</text>
<text x="50.0" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[0]</text>
<text x="90.0" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[1]</text>
<text x="130.0" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[2]</text>
<text x="170.0" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[3]</text>
<text x="210.0" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[4]</text>
<text x="250.0" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[5]</text>
<text x="290.0" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[6]</text>
<path d="M 210.0 76 Q 230.0 102 250.0 76" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250.0,76.0 249.8,83.0 244.5,80.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="230.0" y="101.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 阶</text>
<path d="M 170.0 50 Q 208.0 4 246.0 50" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="246.0,50.0 240.3,45.9 245.6,43.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="208.0" y="24.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 阶</text>
<text x="170" y="144" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[i] = f[i-1] + f[i-2]；求最小花费换成 min(…) + 代价</text>
</svg>

```python
def count_ways(n, steps=(1, 2)):
    f = [0] * (n + 1)
    f[0] = 1                     # 站在起点：一种（什么都不做）
    for i in range(1, n + 1):    # 最后一步迈了 s 阶
        f[i] = sum(f[i - s] for s in steps if s <= i)
    return f[n]

def min_cost(cost):              # 离开第 i 阶要付 cost[i]
    a = b = 0                    # f[i-2], f[i-1]；起点免费
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b                     # 顶部是下标 n
```

**要点。**
- 为什么对？：走到 `i` 的最后一步只有几种可能，之前的走法互不重叠，所以相加就是方案数；求最值同理，从各来源里挑最优。
- LC 746 怎么改？：`sum` 换成 `min`，每个来源再加离开那一阶的费用；终点是下标 `n`，不是 `n - 1`。
- LC 377 怎么改？：`steps` 就是 `nums`，`n` 就是 `target`，外层枚举和、内层枚举数，算的是有序序列；内外对调就成了不计顺序的组合数。

**易错点。**
- `f[0]` 写成 `0`：整张表全是 `0`。
- 终点写成 `n - 1`：`[10,15,20]` 得 `10`，应为 `15`。
- 漏掉 `s <= i`：负下标读到数组尾部，不报错但结果错。

**对应题目。** LC 70 爬楼梯、LC 746 使用最小花费爬楼梯、LC 377 组合总和 Ⅳ
