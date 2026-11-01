---
id: hi-x-transactional-outbox-4-pitfall
node: sd.cross.transactional-outbox
type: qa
step: 4
---
## Q
**事务外盒与可靠发布事件 (Transactional Outbox)**｜跨题模式 · 易错

使用事务外盒时，候选人常犯哪些错？每个错会造成什么具体故障？

## A
1. **仍然"先写库、再直接发消息"。** 崩在两步之间，状态已变而事件丢了，下游永远不知道（商户收不到支付成功回调）。必须把事件行写进同一事务。
2. **以为 outbox 等于恰好一次。** 中继发出后、标记已发送前崩溃，会重发。消费者不按业务键去重，就会重复入账：同一个 `gift_id` 的收益被汇总两次，同一个 `transfer_id` 被入账两次。
3. **对外发送没有稳定的引用号。** outbox 重发给交易所，没有 `orderId` 作为客户端引用号，交易所会收两张单。（[[stock-trading-platform|股票交易平台]]）
4. **所有通知一视同仁都走 outbox。** 拍卖里每次被超越都强保证送达，成本高而收益低；该强保证的是赢家和付款消息。（[[tt-realtime-auction-bidding|实时竞价拍卖]]）
5. **对外部商户的积压放在共享队列里。** 一个商户宕机一小时就是几十万条，堵住同分区别的商户。积压应放在投递表，按端点限并发。（[[tt-merchant-webhook-delivery|商户回调投递系统]]）
6. **跨分片转账只做了第一半。** 转出分片扣了，outbox 事件到达时对方账户已冻结，没有补偿就卡在在途。要有 PENDING→DEBITED→CREDITED 或 REFUNDED 的状态机。（[[tt-wallet-ledger-service|钱包与复式账本服务]]）
