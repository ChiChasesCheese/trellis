---
slug: best-time-to-buy-and-sell-stock
---
## Q
**LC 121 买卖股票的最佳时机**｜Easy

`prices[i]` 是第 `i` 天的股价，只能买一次、卖一次（先买后卖），求最大利润，不能获利返回 `0`。

## A
**一句话。** 一遍扫描维护迄今最低价，把每天当作卖出日，取 `p - low` 的最大值。

**图解。** 虚线是迄今最低价 `low`，每天都算一次 `p - low`，最大的是第 4 天卖出。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 172">
<rect x="40" y="46" width="24" height="84" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="52.0" y="42" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">7</text>
<text x="52.0" y="144" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第0天</text>
<rect x="80" y="118" width="24" height="12" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="92.0" y="114" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1</text>
<text x="92.0" y="144" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第1天</text>
<rect x="120" y="70" width="24" height="60" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="132.0" y="66" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">5</text>
<text x="132.0" y="144" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第2天</text>
<rect x="160" y="94" width="24" height="36" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="172.0" y="90" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">3</text>
<text x="172.0" y="144" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第3天</text>
<rect x="200" y="58" width="24" height="72" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="212.0" y="54" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">6</text>
<text x="212.0" y="144" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第4天</text>
<rect x="240" y="82" width="24" height="48" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="252.0" y="78" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">4</text>
<text x="252.0" y="144" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第5天</text>
<line x1="80" y1="118" x2="270" y2="118" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="272" y="122" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">low</text>
<polyline points="92.0,102 210.0,44" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210.0,44.0 205.9,49.3 203.3,44.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="144.0" y="56" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)" font-weight="600">+5</text>
<text x="150" y="166" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每天当卖出日：p − low，取最大</text>
</svg>

```python
def max_profit(prices):
    low, best = prices[0], 0     # low：迄今最低价
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 用全局最大减全局最小：`[3,10,1]` 得 `9`，最低点在最高点之后，应为 `7`。
- `best` 初始化成负数：不能获利时应返回 `0`。

**追问。**
- 可以交易任意多次（LC 122）？：累加所有相邻正差，`[7,1,5,3,6,4]` 得 `7`。
- 最多 `k` 次（LC 188）或有冷冻期（LC 309）？：状态机 DP，每天维护「持有 / 不持有」的最优值。

**同模式。** LC 122 买卖股票的最佳时机 II、LC 123 买卖股票的最佳时机 III、LC 188 买卖股票的最佳时机 IV、LC 309 买卖股票的最佳时机含冷冻期
