---
id: hft-fees-tick-size-inverted
node: microstructure.fees-tick-size
type: qa
step: 2
---
## Q
反向费率交易所（inverted venue，也叫 taker-maker）和 maker-taker 有什么不同？它们为什么存在？

## A
反向模式正好相反：**taker 得返佣，maker 付费**。美股里 Nasdaq BX、Cboe BYX 等交易所采用过这种模式。

为什么存在：它们想吸引"想立刻成交"的订单，向挂单一方收费。

对 HFT 的影响：
- 挂单方要付费，所以只有"排队位置很有价值"或"成交概率很高"的人才愿意在那里挂单；
- 主动方得到返佣，成交成本降低，所以路由时常把这类交易所放在前面；
- 做市商比较多个交易所时，看的是**净价格**（价格加上费用或返佣），而不只是报价。
