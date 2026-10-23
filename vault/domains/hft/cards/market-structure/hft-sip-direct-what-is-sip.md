---
id: hft-sip-direct-what-is-sip
node: market-structure.sip-direct
type: qa
step: 1
---
## Q
美股的汇总行情系统（SIP，Securities Information Processor）是什么？它和交易所直连行情（direct feed）的数据流程有什么区别？

## A
**SIP：** 法定的"官方"行情汇总者。每个交易所把自己的报价和成交上报给 SIP，SIP 把所有场所的数据合在一起，算出全国最优买卖价（NBBO）和统一的成交记录，再广播给订阅者。美股有两套：一套负责 NYSE 上市的股票等，一套负责 Nasdaq 上市的股票。

**直连行情：** 交易所自己把本场所的原始行情（通常是逐笔订单）直接发给订阅者，不经过任何汇总。

| | SIP | 直连行情 |
|---|---|---|
| 内容 | 汇总后的最优价和成交 | 单个交易所的完整细节 |
| 路径 | 交易所 → SIP → 订阅者 | 交易所 → 订阅者 |
| 价格 | 便宜，人人可用 | 贵，每个交易所单独订 |
