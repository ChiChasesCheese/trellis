---
id: hft-adverse-selection-markout
node: microstructure.adverse-selection
type: qa
step: 2
---
## Q
什么是 markout？如何用它衡量一笔成交的质量？

## A
markout 是成交之后过一段固定时间（如 1 秒、5 秒、1 分钟），用那一刻的中间价（mid）重新评估这笔成交的盈亏。
- 做市商买入：markout = 之后的 mid − 买入价；
- 做市商卖出：markout = 卖出价 − 之后的 mid。

例子：做市商在 99.99 买入 100 股，1 秒后 mid 变成 99.96，markout = (99.96 − 99.99) × 100 = −3 美元；如果 mid 变成 100.02，则是 +3 美元。

用法：把大量成交按对手类型或订单类型分组，求平均 markout。平均为负的是亏钱的订单流，平均为正的是好客户。比较不同时间尺度（1 毫秒、1 秒、1 分钟）的 markout，可以区分是毫秒级的速度型逆向选择，还是较长期的信息影响。
