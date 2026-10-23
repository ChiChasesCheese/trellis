---
id: hft-fees-tick-size-tick
node: microstructure.fees-tick-size
type: qa
step: 3
---
## Q
最小报价单位（tick size）如何决定价差下限和排队长度？

## A
tick 是价格能变动的最小步长：美股价格不低于 1 美元的股票，tick 是 0.01 美元，所以价差最小 1 美分，报价只能落在整数美分上。
- 看相对大小：0.01 的 tick 对 10 美元的股票是 0.1%（10 bp），对 100 美元的股票是 0.01%（1 bp）。
- 股价低、tick 相对很大：价差很难再窄，做市商每股毛利高，排队队伍短。
- 股价高、tick 相对很小：价差常常就是 1 tick（被 tick 限制，tick-constrained），买一价上排很长的队，竞争变成排队速度。

所以 tick 是"价格竞争"和"排队竞争"之间的旋钮。
