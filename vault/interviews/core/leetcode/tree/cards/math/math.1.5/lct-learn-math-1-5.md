---
id: lct-learn-math-1-5
node: math.1.5
type: qa
step: 1
---
## Q
**数学算法 › 数论 › 因子**｜学习卡

套路是什么？

## A
**一句话。** 设 `k` 项、首项 `a`，则 `n = k·a + k(k-1)/2`；枚举项数 `k`，看剩余部分能否被 `k` 整除，`k` 只到 `O(√n)`。

下图：`15 = 4 + 5 + 6`，拆成 `k × a` 的矩形加一个三角形。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="40" y="112" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="40" y="94" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="40" y="76" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="40" y="58" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="80" y="112" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="80" y="94" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="80" y="76" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="80" y="58" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="80" y="40" width="40" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="120" y="112" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="120" y="94" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="120" y="76" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="120" y="58" width="40" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="120" y="40" width="40" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="120" y="22" width="40" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<line x1="40" y1="130" x2="40" y2="136" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="160" y1="130" x2="160" y2="136" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="40" y1="130" x2="160" y2="130" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="100.0" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">k = 3 项，首项 a = 4</text>
<text x="185" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">n = k·a + k(k-1)/2</text>
<text x="185" y="60" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">15 = 3·4 + 3</text>
<text x="185" y="86" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">浅色：k × a 的矩形</text>
<text x="185" y="102" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">深色：0 + 1 + … + (k-1)</text>
<text x="185" y="128" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">枚举 k，看 n - k(k-1)/2</text>
<text x="185" y="144" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">能否被 k 整除</text>
</svg>

```python
def consecutive_numbers_sum(n):
    cnt = 0
    k = 1                            # 项数
    while k * (k + 1) // 2 <= n:     # 首项 >= 1 时的最小和
        if (n - k * (k - 1) // 2) % k == 0:
            cnt += 1                 # 首项 a 是正整数
        k += 1
    return cnt
```

**要点。**
- 为什么对？：`k` 项首项为 `a` 的和是 `k·a + k(k-1)/2`，`a` 必须是正整数，所以 `n - k(k-1)/2` 要正且被 `k` 整除；`a >= 1` 要求 `k(k+1)/2 <= n`，`k` 到不了 `n`。
- 要输出具体序列怎么改？：对合法的 `k` 算出 `a = (n - k(k-1)/2) // k`，输出 `range(a, a + k)`。

**易错点。**
- 循环写成 `k <= n`：线性枚举 `10^9` 次超时。
- 条件放宽成 `k(k-1)/2 <= n`：首项可能为 `0`，`n = 3` 得 `3`，应为 `2`。

**对应题目。** LC 829 连续整数求和
