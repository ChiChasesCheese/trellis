---
id: lct-learn-math-1-4
node: math.1.4
type: qa
step: 1
---
## Q
**数学算法 › 数论 › 阶乘分解**｜学习卡

套路是什么？

## A
**一句话。** 阶乘里每个质因子 `p` 的指数是 `n//p + n//p² + n//p³ + ...`；末尾的零由 `2×5` 配对，`5` 比 `2` 少，只数 `5`。

下图：`n = 25`，每个 5 的倍数贡献一个 5，25 的倍数再多贡献一个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<line x1="20" y1="70" x2="320" y2="70" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<circle cx="80" cy="70" r="5" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="80" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="140" cy="70" r="5" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="140" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<text x="140" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="200" cy="70" r="5" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="200" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">15</text>
<text x="200" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="260" cy="70" r="5" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="260" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">20</text>
<text x="260" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="320" cy="70" r="5" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="320" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">25</text>
<text x="320" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">5</text>
<text x="320" y="42" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">+5</text>
<text x="20" y="18" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">25! 的因子 5：25//5 + 25//25 = 5 + 1 = 6</text>
<text x="170" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">末尾零 = min(2 的个数, 5 的个数) = 5 的个数</text>
</svg>

```python
def trailing_zeroes(n):
    cnt = 0
    while n:
        n //= 5                      # 1..n 里 5^k 的倍数个数
        cnt += n
    return cnt
```

**要点。**
- 为什么对？：`1..n` 中 `5` 的倍数有 `n//5` 个，每个至少一个 `5`；其中 `25` 的倍数多一个，依次类推，逐层累加。
- 末尾零是 `b` 进制的怎么改？：分解 `b = ∏ p^e`，对每个 `p` 求 `n!` 中 `p` 的指数，除以 `e` 取下整，再取所有 `p` 的最小值。

**易错点。**
- 只数 `n // 5`：`n = 25` 得 `5`，漏了 `25` 的第二个 `5`，应为 `6`。
- 真的去算 `n!`：位数巨大，也不是对数时间。

**对应题目。** LC 172 阶乘后的零
