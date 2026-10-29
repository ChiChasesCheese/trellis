---
id: tlc-best-time-to-buy-and-sell-stock-ii-4-followup
node: a.best-time-to-buy-and-sell-stock-ii
type: qa
step: 4
---
## Q
**LC 122 买卖股票的最佳时机 II**｜追问

面试官接着问：（1）每次交易收手续费 `fee`？（2）卖出后要冷却一天？（3）最多只能交易 `k` 次？

## A
1. **手续费（LC 714）**：贪心失效（逐日交易会重复付费）。用 DP：`cash = max(cash, hold + p - fee)`，`hold = max(hold, cash - p)`；卖出时扣一次手续费。`O(n)`。
2. **冷却一天（LC 309）**：买入必须发生在「前天以前」就不持股之后。`hold = max(hold, cash_two_days_ago - p)`，需要多保留一个前天的现金值，或者用三个状态（持有 / 刚卖出冷却 / 可买）。`O(n)`。
3. **至多 `k` 次（LC 123 / 188）**：状态变成 `hold[j]`、`cash[j]`（已完成 `j` 笔交易），`O(nk)`。当 `k ≥ n / 2` 时每天最多一次买卖都放得下，退化成此处的贪心。

**对照** 此处的贪心是 DP 在「约束为空」时的化简；一遇到约束就回到 `cash` / `hold` 状态机。

**Python 提醒**：`itertools.pairwise` 需要 Python 3.10+；老版本写 `zip(prices, prices[1:])`，注意切片会复制 `O(n)` 的列表。`sum` 配生成器表达式不会建中间列表，比先 `[...]` 再 `sum` 省内存。
