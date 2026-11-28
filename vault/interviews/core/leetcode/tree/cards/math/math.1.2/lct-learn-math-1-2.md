---
id: lct-learn-math-1-2
node: math.1.2
type: qa
step: 1
---
## Q
**数学算法 › 数论 › 预处理质数（筛质数）**｜学习卡

套路是什么？

## A
**一句话。** 埃氏筛：从小到大扫，遇到仍是质数的 `i`，把 `i*i` 起的所有倍数划掉，一次预处理 `O(MX log log MX)`，之后质数表和判定都是 `O(1)`。

下图：筛到 31，实心格是留下的质数；更小的倍数早被更小的质数划掉。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="15" y="15" width="31" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="30.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="46" y="15" width="31" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="61.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="77" y="15" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="92.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="108" y="15" width="31" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="123.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<rect x="139" y="15" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="154.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="170" y="15" width="31" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="185.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">7</text>
<rect x="201" y="15" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="216.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<rect x="232" y="15" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="247.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<rect x="263" y="15" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="278.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<rect x="294" y="15" width="31" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="309.5" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">11</text>
<rect x="15" y="47" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="30.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12</text>
<rect x="46" y="47" width="31" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="61.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">13</text>
<rect x="77" y="47" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="92.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">14</text>
<rect x="108" y="47" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="123.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">15</text>
<rect x="139" y="47" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="154.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">16</text>
<rect x="170" y="47" width="31" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="185.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">17</text>
<rect x="201" y="47" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="216.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">18</text>
<rect x="232" y="47" width="31" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="247.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">19</text>
<rect x="263" y="47" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="278.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">20</text>
<rect x="294" y="47" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="309.5" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">21</text>
<rect x="15" y="79" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="30.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">22</text>
<rect x="46" y="79" width="31" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="61.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">23</text>
<rect x="77" y="79" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="92.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">24</text>
<rect x="108" y="79" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="123.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">25</text>
<rect x="139" y="79" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="154.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">26</text>
<rect x="170" y="79" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="185.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">27</text>
<rect x="201" y="79" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="216.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">28</text>
<rect x="232" y="79" width="31" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="247.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">29</text>
<rect x="263" y="79" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="278.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">30</text>
<rect x="294" y="79" width="31" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="309.5" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">31</text>
<text x="170" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">遇到质数 i：从 i·i 起把倍数划掉（虚框）</text>
</svg>

```python
MX = 1_000_001
is_prime = [False] * 2 + [True] * (MX - 2)   # 0 和 1 不是质数
primes = []
for i in range(2, MX):
    if is_prime[i]:
        primes.append(i)
        for j in range(i * i, MX, i):        # 更小的倍数早被划掉
            is_prime[j] = False
```

**要点。**
- 为什么对？：合数 `x` 的最小质因子 `p` 满足 `p * p <= x`，所以 `x` 必在 `p` 划倍数（从 `p * p` 起）时被划掉。
- LC 204 怎么改？：范围是 `[0, n)`，把 `MX` 换成 `n`，答案是 `sum(is_prime)`。
- LC 2523 怎么改？：筛出区间内的质数，最近的一对必是相邻质数，扫一遍取差最小、位置靠前的。

**易错点。**
- 起点写成 `2 * i`：结果仍对，但会多做很多重复划线。
- 204 的范围不含 `n`：筛的大小取 `n`，`n = 10` 应得 `4`（2、3、5、7），取 `n + 1` 会多算 `n` 本身。
- 2523 并列取小：差相同时取先出现的一对，比较用严格小于，`[11, 13, 17]` 应得 `[11, 13]`。

**对应题目。** LC 2523 范围内最接近的两个质数、LC 204 计数质数
