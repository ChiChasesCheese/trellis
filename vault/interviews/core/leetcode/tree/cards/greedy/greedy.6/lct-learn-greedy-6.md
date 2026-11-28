---
id: lct-learn-greedy-6
node: greedy.6
type: qa
step: 1
---
## Q
**贪心算法 › 构造题**｜学习卡

套路是什么？

## A
**一句话。** 构造题：先造出最小结构满足条件，再用不改变条件的方式补齐。前 `k+1` 个数在 `1..k+1` 里一头一尾交替取，相邻差恰为 `k, k-1, ..., 1`。

下图：LC 667（n = 6，k = 3），先造出恰有 `k` 种差的最小结构，再补齐。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="30" y="40" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="53.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="76" y="40" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="99.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<rect x="122" y="40" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="145.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="168" y="40" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="191.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="214" y="40" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="237.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="260" y="40" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="283.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="76.0" y="86" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">差 3</text>
<text x="122.0" y="86" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">差 2</text>
<text x="168.0" y="86" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">差 1</text>
<text x="214.0" y="86" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">差 2</text>
<text x="260.0" y="86" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">差 1</text>
<line x1="30" y1="34" x2="30" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="214" y1="34" x2="214" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="30" y1="34" x2="214" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="122.0" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1..k+1 一头一尾交替（k = 3）</text>
<text x="170" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">前 k+1 个：相邻差恰为 k, k-1, …, 1</text>
<text x="170" y="130" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">其余顺序补齐：差值都已出现过，不引入新差值</text>
</svg>

```python
def construct_array(n, k):
    ans = []
    lo, hi = 1, k + 1
    while lo <= hi:
        ans.append(lo)               # 一头一尾交替
        lo += 1
        if lo <= hi:                 # 两端相遇时别重复加
            ans.append(hi)
            hi -= 1
    ans.extend(range(k + 2, n + 1))  # 只产生差 1，不引入新差值
    return ans
```

**要点。**
- 为什么对？：交替取 `1, k+1, 2, k, ...` 的相邻差依次是 `k, k-1, ..., 1`，共 `k` 种；后面递增接上只多出差 `1`，已经有了。
- LC 280 怎么改？：排序后交换 `(1,2)`、`(3,4)` 这几对相邻元素，让奇数位成峰：`for i in range(1, n - 1, 2)`。

**易错点。**
- 交替取数铺满整个 `1..n`：`n = 5`、`k = 2` 得 `[1,5,2,3,4]`，差集合有 `3` 种。
- 漏掉后面的 `extend`：`n = 5`、`k = 2` 只返回 `[1,3,2]`，长度不足。
- LC 280 循环写成 `range(1, n, 2)`：`n` 为偶数时 `i + 1` 越界。

**对应题目。** LC 280 摆动排序、LC 667 优美的排列 II
