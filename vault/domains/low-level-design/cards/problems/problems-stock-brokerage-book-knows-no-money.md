---
id: problems-stock-brokerage-book-knows-no-money
node: problems.marketplaces.stock-brokerage
type: qa
step: 1
tags: [grown]
---
## Q
在股票交易系统（stock brokerage）设计里，订单簿（order book，挂着所有未成交买卖单的那本簿子）该不该负责扣钱过户？这一刀切在哪里，能换来什么？

## A
**不该。订单簿只认股数，一分钱都不碰。**

切法是两层：

- `OrderBook` / `BookSide`：谁排在谁前面、这一笔成交多少股、成交价是多少。它的输出是一串 `(对手挂单, 成交价, 成交股数)`。
- `Brokerage`（门面 Facade）：账户、资金与持仓校验、按这串结果逐笔结算、成交流水、行情推送。

换来三件事：撮合规则可以脱离钱被单独测试（撮合是纯粹的排序与配对）；资金规则怎么改（加手续费、加融资融券、改结算周期）都动不到撮合的任何一行；以及最实际的——撮合出错和记账出错在栈里是两个地方，不会混成一团。

反面写法是在撮合循环里直接 `buyer.debit(...)`、`seller.credit(...)`，流行题解大多如此：一旦钱不够就得把已经改过的对手单和簿子结构回滚回去，而那几乎必然写错。
