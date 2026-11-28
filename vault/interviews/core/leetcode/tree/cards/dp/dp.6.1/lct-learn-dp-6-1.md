---
id: lct-learn-dp-6-1
node: dp.6.1
type: qa
step: 1
---
## Q
**动态规划 › 状态机 DP › 买卖股票**｜学习卡

套路是什么？

## A
**一句话。** 状态机 DP：每天只有「持有」和「空仓」两种状态，买入才消耗一笔交易，所以交易次数 `k` 进 `buy` 的下标，卖出回到空仓。

下图：每天只在「空仓」「持有」两个状态之间转移。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="37.0" y="55.0" width="86" height="40" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sell[j]</text>
<text x="80" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">空仓</text>
<rect x="217.0" y="55.0" width="86" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">buy[j]</text>
<text x="260" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">持有</text>
<path d="M 123 62 L 217 62" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="217.0,62.0 210.7,65.0 210.7,59.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="54" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">买入：sell[j-1] − p</text>
<path d="M 217 88 L 123 88" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="123.0,88.0 129.3,85.0 129.3,91.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="104" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">卖出：buy[j] + p</text>
<path d="M 60 55 C 40 20, 100 20, 95 53" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="95.0,53.0 92.9,46.3 98.9,47.2" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="80" y="22" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不动</text>
<path d="M 240 55 C 220 20, 280 20, 275 53" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="275.0,53.0 272.9,46.3 278.9,47.2" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="260" y="22" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不动</text>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">只有买入消耗一笔交易：j 跟着买入走</text>
<text x="170" y="158" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">答案 sell[n][k]：最后必须空仓</text>
</svg>

```python
def max_profit(k, prices):       # 最多 k 笔
    n = len(prices)
    # buy[i][j]：前 i 天、手里有货、已买 j 笔的最大现金
    buy = [[-inf] * (k + 1) for _ in range(n + 1)]
    # sell[i][j]：前 i 天、空仓、至多买 j 笔的最大现金
    sell = [[0] * (k + 1) for _ in range(n + 1)]
    for i, p in enumerate(prices):
        for j in range(1, k + 1):
            buy[i+1][j] = max(buy[i][j], sell[i][j-1] - p)
            sell[i+1][j] = max(sell[i][j], buy[i][j] + p)
    return sell[n][k]
```

**要点。**
- 为什么对？：买入从「少一笔的空仓」转来，笔数加一；卖出回到空仓，笔数不变。第 `0` 天不可能有货，所以 `buy` 初值是 `-inf`。
- LC 122（不限次）怎么改？：贪心：所有相邻正差价之和；`k >= n // 2` 时 LC 188 也退化成它。
- LC 123 怎么改？：`k = 2` 直接套用。
- LC 309、714 怎么改？：不限次，去掉笔数维：309 买入只能从两天前的空仓转来（卖出后冷冻一天）；714 卖出时多减 `fee`。

**易错点。**
- `buy` 初值写 `0`：等于免费拿到股票，`(2, [3,2,6,5,0,3])` 得 `9`，应为 `7`。
- 买入从 `sell[i][j]` 转移：不占新笔数，`k` 的限制失效，必须读 `sell[i][j-1]`。
- 答案取 `buy[n][k]`：未卖出的持仓不是已实现利润，取 `sell[n][k]`。

**对应题目。** LC 122 买卖股票的最佳时机 II、LC 123 买卖股票的最佳时机 III、LC 188 买卖股票的最佳时机 IV、LC 309 买卖股票的最佳时机含冷冻期、LC 714 买卖股票的最佳时机含手续费
