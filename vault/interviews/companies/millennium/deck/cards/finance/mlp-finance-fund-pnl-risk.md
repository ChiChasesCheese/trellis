---
id: mlp-finance-fund-pnl-risk
node: finance.fund
step: 2
type: qa
---
## Q
**盈亏、风险限额与回撤**｜金融常识

"什么是 PnL？pod 的风险限额和回撤（drawdown）是什么意思？"

## A
**PnL（profit and loss，盈亏）** 是持仓在一段时间里赚或亏了多少。持仓的盈亏等于价格变化乘以数量；已卖出落袋的叫已实现盈亏（realized），还持有的按当前市价估算，叫未实现盈亏（unrealized）。持仓以外币计价时，还要乘上当天的汇率，所以多币种盈亏是 `Δ(价格 × 数量 × 汇率)`。

**风险限额（risk limit）** 是风控给每个 pod 划的边界，例如持仓规模、集中度、杠杆上限。超限就不能再加仓，甚至要强制减仓。

**回撤（drawdown）** 是从净值高点到之后低点的最大跌幅。多策略基金对 pod 的回撤限制很严：回撤触及限额，资金会被削减甚至整个团队被关掉。所以每个 pod 都在严格管理亏损，而不只是追求赚钱。

**对数据工程师意味着什么。**
- **盈亏取决于价格与汇率的时间点：** 价格或汇率取错时点，盈亏就错，风控就会据此误判。
- **限额要快：** 风控要尽快看到汇总的仓位和盈亏，数据延迟直接变成风险敞口。
- **历史要可复现：** 回撤和归因要在任何时候重算出同样的结果。

**英文答法。**
- "**PnL** is price change times quantity, converted at that day's FX rate."
- "Pods have **tight drawdown limits**, so correct and timely data matters for risk."
