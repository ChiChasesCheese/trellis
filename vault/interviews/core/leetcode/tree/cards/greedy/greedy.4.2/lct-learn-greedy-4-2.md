---
id: lct-learn-greedy-4-2
node: greedy.4.2
type: qa
step: 1
---
## Q
**贪心算法 › 数学贪心 › 乘积贪心**｜学习卡

套路是什么？

## A
**一句话。** 乘积的最大值只出在两端：最大的三个数，或最小的两个（两负得正）乘最大的一个。

下图：LC 628，排序后只有两个候选：三个最大，或两个最小乘最大。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="45" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="70.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">-5</text>
<rect x="95" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="120.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">-4</text>
<rect x="145" y="40" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="195" y="40" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="220.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="245" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="270.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<line x1="145" y1="34" x2="145" y2="28" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="295" y1="34" x2="295" y2="28" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="145" y1="34" x2="295" y2="34" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="220.0" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三个最大：1·2·3 = 6</text>
<line x1="45" y1="74" x2="45" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="145" y1="74" x2="145" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="45" y1="74" x2="145" y2="74" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="95.0" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两个最小</text>
<text x="170" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">(-5)·(-4)·3 = 60：两负得正</text>
<text x="170" y="132" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">答案只可能出在排序后的两端</text>
</svg>

```python
def maximum_product(nums):
    nums.sort()
    return max(nums[-1] * nums[-2] * nums[-3],   # 三个最大
               nums[0] * nums[1] * nums[-1])     # 两个最小 × 最大
```

**要点。**
- 为什么对？：负数个数为偶数乘积才为正：全正取最大三个；有负数时，最负的两个相乘变成大正数再乘最大值；其他取法都不会更大。
- 选 `k` 个数怎么改？：排序后两端各取一对，枚举取几对（以及奇数 `k` 时先取最大值）。

**易错点。**
- 只取最大的三个：`[-10,-10,1,3,2]` 得 `6`，应为 `300`。
- 扫描法里最大值初值设成 `0`：`[-1,-2,-3]` 得 `0`，应为 `-6`。

**对应题目。** LC 628 三个数的最大乘积
