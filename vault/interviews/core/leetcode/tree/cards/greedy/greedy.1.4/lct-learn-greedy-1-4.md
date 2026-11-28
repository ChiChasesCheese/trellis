---
id: lct-learn-greedy-1-4
node: greedy.1.4
type: qa
step: 1
---
## Q
**贪心算法 › 贪心策略 › 从最左/最右开始贪心**｜学习卡

套路是什么？

## A
**一句话。** 从最左（或最右）一格一格扫，当场做出局部最优决定，且不影响已经决定的部分。

下图：LC 605，一格一格扫，能种就种。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 120">
<rect x="20" y="40" width="33" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="36.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="53" y="40" width="33" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="69.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="40" width="33" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="102.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="119" y="40" width="33" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="135.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">种</text>
<rect x="152" y="40" width="33" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="168.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="185" y="40" width="33" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="201.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="218" y="40" width="33" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="234.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="251" y="40" width="33" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="267.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">种</text>
<rect x="284" y="40" width="33" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="300.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="36.5" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">补 0</text>
<text x="300.5" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">补 0</text>
<text x="170" y="96" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">从左往右：左、自己、右都是 0 就立刻种</text>
<text x="170" y="114" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">种了会挡住下一格，但不会动已经决定的格子</text>
</svg>

```python
def can_place_flowers(flowerbed, n):
    bed = [0, *flowerbed, 0]         # 两端补 0，免边界特判
    for i in range(1, len(bed) - 1):
        if bed[i - 1] == bed[i] == bed[i + 1] == 0:
            bed[i] = 1               # 能种就种，会影响下一格
            n -= 1
    return n <= 0
```

**要点。**
- 为什么对？：每个空位尽量靠左种，对右边的约束最小，所以第一个能种的位置就种。
- LC 1827 怎么改？：一趟扫描，每个数至少抬到「调整后的前一个数 + 1」：`t = max(x, prev + 1)`，累加 `t - x`，`prev = t`。

**易错点。**
- 种完不把 `bed[i]` 改成 `1`：`([0,0], 2)` 两格都被判可种，返回 `True`，应为 `False`。
- LC 1827 的 `prev` 记成原始的 `x`：`[1,5,2,4,1]` 得 `8`，应为 `14`。

**对应题目。** LC 605 种花问题、LC 1827 最少操作使数组递增
