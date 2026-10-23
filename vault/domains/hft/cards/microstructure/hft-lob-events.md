---
id: hft-lob-events
node: microstructure.lob
type: qa
step: 4
---
## Q
订单簿是怎样随着行情消息更新的？为什么行情消息的数量远大于成交的数量？

## A
订单簿由一串**事件**驱动：新增订单（add）、撤销（cancel）、修改（replace）、成交（execute）。行情就是把这些事件按序号发给订阅者，你的程序按顺序重放，就能重建出和交易所一模一样的订单簿。

例子：Nasdaq ITCH 协议里有 Add Order、Order Executed、Order Cancel、Order Delete、Order Replace 等消息。

比例：绝大多数订单从未成交就被撤掉或改掉，所以消息里新增和撤销占绝对多数，成交只占很小一部分。

后果：行情系统要跟上的是事件流的速度，而不是成交笔数。整个市场峰值可达每秒百万条量级，每条消息可用的处理时间只有约 1 µs。而且消息带序号，丢一条，订单簿就错了。
