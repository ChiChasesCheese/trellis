---
id: hl-business-market-maker
node: company.business
type: qa
step: 5
---
## Q
做市商（market maker）怎么赚钱，又给市场提供了什么？为什么做市必须全自动？

## A
做市商**同时在买一和卖一附近挂单**：有人想马上卖就买他的，有人想马上买就卖给他。

- 赚的是**价差**（spread）。例：99.99 买入 1000 股、100.01 卖出 1000 股，赚 1000 × 0.02 = **$20**。
- 提供**流动性**（liquidity）：任何时候想成交都有对手。
- 一次只赚 $20，所以要做**海量次数**，人工做不过来，必须全自动。

Headlands 的三类策略是套利（arbitrage）、主动吃单（market taking）和做市，做市是其中之一。
