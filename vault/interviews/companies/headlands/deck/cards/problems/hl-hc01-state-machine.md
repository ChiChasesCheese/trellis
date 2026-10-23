---
id: hl-hc01-state-machine
node: problems.hc01-stock-trading-dp
type: qa
step: 5
---
## Q
买卖股票的状态机（finite state machine）有哪几个状态、每天有哪些箭头？加冷却和加「最多 k 笔」分别怎么改图？

## A
基本两个状态：
- `FREE`：手里**没有**股票（可买）；
- `HOLD`：手里**有**一股（可卖）。

每天三选一：休息（留在原状态）、买（FREE→HOLD，现金减价格）、卖（HOLD→FREE，现金加价格）。

**加冷却**：多一个状态 `COOL`（今天刚卖出，明天只能休息）。卖出箭头 HOLD→COOL；COOL→FREE 是被迫休息；买入只能从 FREE 出发，不能从 COOL 买。

**加「最多 k 笔」**：每个状态加下标 j=「已用几次买入」，图复制成 k+1 层，买入箭头从第 j−1 层指向第 j 层。

为什么先画图：转移就是把每条箭头翻译成一行代码，漏箭头、多箭头一眼可见。Java 里用 `enum State { FREE, HOLD, COOL }`，每类箭头一个方法：`afterRest()`、`afterBuy()`、`afterSell(rules)`。
