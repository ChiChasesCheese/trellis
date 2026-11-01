---
id: hi-pt-stock-trading-platform-4-place-order-txn
node: qb.sd.stock-trading-platform.points
type: qa
step: 4
---
## Q
**股票交易平台（券商端） · 下单事务里的三件事**｜出自：股票交易平台（券商端） › 整体设计

下单时订单服务在一个数据库事务里要做哪三件事？事务提交后才做什么？

## A
**三件事。** (1) 冻结资金或股票；(2) 插入 NEW 订单行，`clientRequestId` 唯一约束；(3) 插入一条发件箱记录。
**之后。** 事务提交后才向客户端返回已接收；发件箱投递器把订单推到队列（按代码或账户分区，保证同账户下单与撤单顺序），网关发给交易所。
