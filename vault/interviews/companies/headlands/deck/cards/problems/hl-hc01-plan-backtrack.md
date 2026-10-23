---
id: hl-hc01-plan-backtrack
node: problems.hc01-stock-trading-dp
type: qa
step: 14
---
## Q
股票 DP 怎样回溯（backtracking）还原具体买卖日？决策记录存什么，倒着走时三个状态各做什么？

## A
DP 只给利润数字。还原：正向填表时每个 (天, j) 格记 **2 个比特**：
- bit0：`hold` 是不是「今天买入」得来（`free[j-1]-p > hold[j]` 严格成立）；
- bit1：`free` 是不是不是「休息」得来（来自卖出，或来自冷却结束）。

**平局选休息**（严格 `>`），不产生零利润交易。从终点状态（`FREE` 或 `COOL`，取现金多的）倒着走：
- `COOL`：这天卖出，记卖出日，状态→`HOLD`；
- `HOLD`：bit0=1 → 这天买入，配对记 `(买入日, 刚记的卖出日)`，状态→`FREE`，j 减 1；bit0=0 → 昨天也持有，原地不动；
- `FREE`：bit1=1 → 有冷却是「昨天卖、今天冷却结束」→`COOL`，无冷却是今天卖出 → 记卖出日、→`HOLD`；bit1=0 → 休息。

`[1,2,3,0,2]` 倒走得 `[Trade(3,4), Trade(0,1)]`，反转成 `[Trade(0,1), Trade(3,4)]`。注意：先用**当前 j** 读 bits，买入分支里才 `j--`。

代价：不能再滚动，空间 O(n·min(k,n/2)) 字节；格子数超过 `MAX_PLAN_CELLS`（2²⁸）拒绝。
