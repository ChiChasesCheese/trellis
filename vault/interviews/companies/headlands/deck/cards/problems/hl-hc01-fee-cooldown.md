---
id: hl-hc01-fee-cooldown
node: problems.hc01-stock-trading-dp
type: qa
step: 12
---
## Q
股票 DP 加手续费（LC 714）和冷却（LC 309）分别要改状态机的哪里？冷却版的三条转移怎么写？

## A
**手续费**：只改一处，卖出箭头 `hold + p` 变成 `hold + p − fee`，状态机不变；「买了又立刻卖」亏钱，DP 自动不做。fee 等于价差时净利润为 0，也不应交易；fee 大于所有价差返回 0。

**冷却**：「今天是不是刚卖出」影响明天能否买，所以必须是状态——新增 `COOL`：
- `hold'[j] = max(hold[j], free[j-1] - p)`：买入只能从 FREE 来；
- `cool'[j] = hold[j] + p - fee`：今天卖出进入 COOL（不是 max，因为 COOL 指**今天刚**卖出）；
- `free'[j] = max(free[j], cool[j])`：休息，或昨天卖的今天冷却结束。

无冷却时卖出直接回 FREE：`free' = max(free, hold + p - fee)`。答案：`max(free, cool)`。

验算 `[1,2,3,0,2]`：cool 依次 −∞,1,2,−1,3，最终 `max(2,3)=3`。

**最常见错**：买入读了今天已更新的 `free'`，等于冷却期内买入，同一份数据得到 4 而非 3。买入必须只用「昨天结束时」的 FREE。
