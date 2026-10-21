# hc01 · Best Time to Buy and Sell Stock 家族（动态规划 / 状态机）

## 读题前你需要知道

* **动态规划（dynamic programming, DP）**到底是什么：「状态」(state) 是什么、「转移」(transition) 是什么、为什么只记「每个状态下的最优值」就够了；
* 怎么把「每天买 / 卖 / 休息」画成一台**状态机**（finite state machine），再把画出来的箭头逐条翻译成代码；
* **滚动数组**（rolling array）为什么能把 O(n·k) 的表压成 O(k)，以及它的更新顺序为什么不能乱；
* 为什么要「回溯」(backtracking) 才能还原出具体交易。


## 背景

给你一只股票连续 n 天的收盘价 `prices[i]`（第 i 天，从 0 数起；价格是非负整数，单位是最小报价单位 tick）。
你每次只能持有**一股**；买之前必须先卖掉手里的（不能同时持有两股）；同一天只能做一个动作（买、卖、休息三选一）。
问最多能赚多少钱。题目一步步加规则：

## Part 一览

| Part | 入口（`StockTrading`） | 内容 | 对应 LeetCode |
|---|---|---|---|
| 1 | `maxProfitBrute(long[])` · `maxProfitOnce(long[])` | 只能买卖**一次**：先写 O(n²) 暴力，再改成 O(n) | 121 |
| 2 | `maxProfitUnlimited(long[])` | 次数**不限** | 122 |
| 3 | `maxProfitAtMost(int k, long[])` | 最多 **k 笔**交易：状态机 DP + 滚动数组 | 188（k=2 即 123） |
| 4 | `maxProfit(Rules, long[])` · `plan(Rules, long[])` · `replay(Rules, long[], List<Trade>)` | 同一台状态机加上**冷却** / **手续费**；还原具体的买卖日；写一个检查器回放方案 | 309 · 714 |

`Trade`、`Plan`、`Rules`、`State`（enum：`FREE` / `HOLD` / `COOL`）、`Move`（sealed：`Buy` / `Sell`）在 starter 里已给出（`State` 的三个方法留给你写）。签名以 starter 为准，这里只写语义。

一笔**交易**（transaction）= 一次买入 + 之后的一次卖出。「最多 k 笔」按**买入次数**数。

## Part 1 · 一次交易

* `maxProfitBrute`：试遍所有 (买入日 i, 卖出日 j>i)，取 `prices[j] - prices[i]` 的最大值，至少是 0（可以一笔都不做）。O(n²)，用来给后面的解法当「标准答案」。
* `maxProfitOnce`：O(n) 时间，O(1) 空间。
* 输入校验（**所有 Part 共用**）：`prices == null` → `NullPointerException`；长度 > `MAX_DAYS`（2²²）或任何价格不在 `[0, MAX_PRICE]`（`MAX_PRICE = 2⁴⁰`）→ `IllegalArgumentException`。
  为什么有上界：这样利润最多 2²¹ × 2⁴⁰ = 2⁶¹，`long` 里永远不会溢出，内循环里不需要 `addExact`。
* 样例：`[7,1,5,3,6,4]` → 5（第 1 天买，第 4 天卖）；`[7,6,4,3,1]` → 0。

## Part 2 · 次数不限

* `maxProfitUnlimited`：可以买卖任意多次（但仍是先卖后买、同一天一个动作）。O(n)。
* 样例：`[7,1,5,3,6,4]` → 7（1→5 赚 4，3→6 赚 3）；`[1,2,3,4,5]` → 4；`[7,6,4,3,1]` → 0。

## Part 3 · 最多 k 笔（状态机 DP）

* `maxProfitAtMost(k, prices)`：最多买入 k 次。`k < 0` → `IllegalArgumentException`；`k == 0` 或 n < 2 → 0。
* **k 可以很大**（`Integer.MAX_VALUE`）：n 天最多完成 n/2 笔，`k ≥ n/2` 时必须退化成 Part 2，不能 `new long[k + 1]`。
* 时间 O(n·min(k, n/2))，空间 O(min(k, n/2))。
* 样例：`k=2, [2,4,1]` → 2；`k=2, [3,2,6,5,0,3]` → 7；`k=2, [3,3,5,0,0,3,1,4]` → 6（LC 123）。

## Part 4 · 冷却 / 手续费 / 还原交易

`Rules(maxTransactions, fee, cooldown)`：

* `fee`：每笔**卖出**时扣的手续费（LC 714）；`fee ∈ [0, MAX_PRICE]`。
* `cooldown`：卖出之后的**下一天**不能买入（LC 309）。
* `maxTransactions`：同 Part 3；`Rules.UNLIMITED` 表示不限。
* 构造时校验：`maxTransactions < 0` 或 `fee` 越界 → `IllegalArgumentException`。

三个入口：

* `maxProfit(rules, prices)`：只要利润数字。
* `plan(rules, prices)` → `Plan(profit, trades)`：利润 + 具体交易。`trades` 按时间排序，每个 `Trade(buyDay, sellDay)`，**每笔净利润（卖价 − 买价 − fee）> 0**（零利润的交易不出现）。
  最优方案可能不唯一，测试只检查「合法 + 利润等于最优」，以及少数方案唯一的样例。
  格子数 `(n+1) × (min(k, n/2)+1)` 超过 `MAX_PLAN_CELLS`（2²⁸）→ `IllegalArgumentException`（还原需要把每格的决定记下来）。
* `replay(rules, prices, trades)`：用 `State` 状态机**逐天回放**一个方案，返回利润（每笔卖出扣 fee）。
  非法 → `IllegalArgumentException`：笔数超过 `maxTransactions`；日期 ≥ n；同一天有两个动作（包括「同一天卖出又买入」）；重叠（持有时又买）；冷却期内买入；卖出时没持有。

`State` 的三个方法：

| 方法 | 规则 |
|---|---|
| `afterRest()` | `COOL → FREE`，其余不变 |
| `afterBuy()` | 只有 `FREE` 能买 → `HOLD`；否则 `IllegalStateException` |
| `afterSell(rules)` | 只有 `HOLD` 能卖 → 有冷却得 `COOL`，没有得 `FREE`；否则 `IllegalStateException` |

### 样例

| rules | prices | 利润 | 说明 |
|---|---|---|---|
| 不限，冷却 | `[1,2,3,0,2]` | 3 | `Trade(0,1)` + `Trade(3,4)`（LC 309） |
| 不限，fee=2 | `[1,3,2,8,4,9]` | 8 | 1→8（赚 7−2=5）+ 4→9（赚 5−2=3）（LC 714） |
| 不限，fee=3 | `[1,3,7,5,10,3]` | 6 | 1→10 一笔，10−1−3 = 6 |
| 不限 | `[7,1,5,3,6,4]` | 7 | `plan` 的交易 = `[Trade(1,2), Trade(3,4)]` |
| 至多 1 笔 | `[7,1,5,3,6,4]` | 5 | `plan` 的交易 = `[Trade(1,4)]` |

## 边界清单（隐藏测试多半打这些）

空数组、1 天、全递减、全相等；最低点在最高点**之后**（别算成全局最大 − 全局最小）；`k = 0`、`k = Integer.MAX_VALUE`、`k = n/2` 临界；
手续费 ≥ 任何价差（一笔都不做）、手续费 == 价差（净利润 0 也不做）；冷却下 `[1,2,1,2]`（不能第 1 天卖、第 2 天买）；
价格 0 与 `MAX_PRICE`；用 `int` 累加利润溢出；`plan` 里买入日必须 < 卖出日、交易不重叠、冷却间隔；`replay` 的各种非法方案。

## 相关变体

* LC 123（正好 k=2）、LC 188（任意 k）、LC 309（冷却）、LC 714（手续费），以及把它们拼在一起的「冷却 + 手续费 + 最多 k 笔」（Part 4 的 `Rules` 就是这个组合）；
* 「你只给我利润不够，把买卖日期也给出来」→ 回溯（Part 4 的 `plan`）；
* 「价格是流式输入，不能存下来」→ 只要利润的话滚动数组本来就是一遍扫描；要还原则需要记录候选买入点；
* 「多只股票、共享本金」→ 已经不是同一个问题（背包 / 带约束优化）；
* 「滑点 / 买卖价差（bid-ask spread）：买用 ask、卖用 bid」→ 把每天的价格拆成两个数组，状态机不变。

## 考什么

不是背 6 道题的解法，而是**会把「每天结束时我可能处于哪几种情况」画成状态机，再逐条箭头翻译成转移**——这样 121、122、123、188、309、714 只是同一台机器的不同参数。
面试官看的是：能不能从暴力出发讲清楚每一步改进；状态定义得清不清楚；k 很大时有没有炸内存；溢出怎么处理；以及「把交易日期还原出来」时回溯写得稳不稳。
