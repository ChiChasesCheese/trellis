---
id: uth-gaps-heuristics-1-filter-score
node: gaps.heuristics
type: qa
step: 1
---
## Q
**装箱太难，调度器怎样放 Pod**｜Kubernetes · 1.37

100 个 Pod 要放进 20 台机器，每个 Pod 要一定的 CPU 和内存，每台机器容量有限。Kubernetes 的调度器（scheduler）怎样决定每个 Pod 去哪一台？

## A
**背景。** 这是装箱（bin packing）问题：东西大小不一，箱子容量有限，要找最好的放法。全局最优要把所有放法都试一遍（20 台放 100 个有 20^100 种），而且 Pod 陆续到来，下一个多大还不知道，全局最优本身就无从谈起。

**结构。** 贪心（greedy）：每次只管眼前这一个 Pod。过滤（filter）：装不下的机器淘汰。打分（score）：给剩下的每台打 0 到 100 分。选分最高的。默认打分 `LeastAllocated`：每种资源得分 =（容量 − 放入后已用）× 100 ÷ 容量，CPU 和内存各算一次，按权重（默认各 1）取平均。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">每台 4 核  浅色 = 已用  P = 新 Pod (要 1 核)</text>
<text x="12" y="50" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">A</text>
<rect x="40" y="34" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="72" y="34" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="34" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="136" y="34" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="34" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="55" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">P</text>
<text x="206" y="50" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">75 分</text>
<text x="12" y="94" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">B</text>
<rect x="40" y="78" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="72" y="78" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="104" y="78" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="136" y="78" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="78" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="119" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">P</text>
<text x="206" y="94" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">25 分</text>
<text x="12" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">C</text>
<rect x="40" y="122" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="72" y="122" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="104" y="122" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="136" y="122" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="168" y="122" width="30" height="22" rx="3" stroke="currentColor" stroke-width="1.8" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="183" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">P</text>
<text x="206" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">装不下 淘汰</text>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">取最高分的节点: A</text>
<text x="170" y="206" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">分数 = (容量 - 放入后已用) x 100 / 容量</text>
</svg>
```

**细节。**

- 图里只看 CPU 一项：A 放入后已用 1 核，得分（4 − 1）× 100 ÷ 4 = 75；B 放入后已用 3 核，得 25；C 放不下
- 分数相同时随机选一台

**为什么。** 每个 Pod 只比一遍机器，速度快、能在线；代价是不保证全局最优，早放的 Pod 不会为后来的让路。

**例题：** LC 474 一和零（同类：LC 416 分割等和子集）

二进制字符串数组 `strs` 和整数 `m`、`n`，求最大的子集，使子集里所有字符串的 `0` 总数不超过 `m`、`1` 总数不超过 `n`。这是两个容量（0 的个数、1 的个数）的 0/1 背包，用 DP 能求出精确最优，代价是规模一大就算不动。`1 <= strs.length <= 600`，`1 <= m, n <= 100`。

```python
def find_max_form(strs: list[str], m: int, n: int) -> int:
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros, ones = s.count("0"), s.count("1")
        for i in range(m, zeros - 1, -1):
            for j in range(n, ones - 1, -1):
                dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)
    return dp[m][n]
```
