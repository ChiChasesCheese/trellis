---
id: hft-architecture-tick-to-trade-colocation-and-distance
node: architecture.tick-to-trade
type: qa
step: 3
---
## Q
tick-to-trade 只计本机处理时间，为什么 HFT 公司还要把服务器放进交易所的机房（co-location）？

## A
因为订单还要走线到交易所的撮合引擎（matching engine），距离本身就是延迟。

光在光纤里约 **5 ns/米**。同机房拉一根 50 m 的光纤只有约 250 ns；而芝加哥到新泽西，微波约 4 ms、光纤约 6.5–7 ms。对比本机软件处理的几微秒，毫秒级的距离会把任何软件优化淹没。

把服务器放进交易所机房后，距离不再是问题，竞争就转到机房内部：每米线缆约 5 ns 都成了可争的项，不少交易所因此让所有客户到撮合引擎的线缆等长，以示公平。这时才轮到把本机 tick-to-trade 压到几微秒甚至更低。
