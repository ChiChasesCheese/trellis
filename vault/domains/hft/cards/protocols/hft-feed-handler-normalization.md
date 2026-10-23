---
id: hft-feed-handler-normalization
node: protocols.feed-handler
type: qa
step: 2
---
## Q
feed handler 为什么要把各交易所的行情归一化（normalize）成内部统一格式？这样做有什么代价？

## A
**为什么：** 每家交易所的协议各不相同：
- Nasdaq 用 ITCH，价格是 4 位小数的整数，有 Stock Locate 编号；
- CME 用 SBE，字节序是小端，价格精度和合约代码规则又不同；
- 有的交易所时间戳是午夜起的纳秒，有的是 UNIX 纪元起的纳秒。

如果让策略直接处理这些差异，每个策略都要写 N 套代码，新增一家交易所就要改所有策略。归一化之后，策略只面对一种结构，比如：`symbolId`（内部整数编号）、`side`、`price`（统一精度的整数）、`qty`、`exchangeTime`。新增交易所只需新增一个 feed handler。

**代价：**
- 多一次拷贝和转换，每条消息约增加几十纳秒。
- 可能丢失某个交易所独有的细节，需要在内部格式里预留扩展位。
- 必须保留原始的交易所时间戳和本机收到的时间，用于延迟测量和问题排查。

通常认为这笔代价值得：换来了策略代码和交易所的解耦。
