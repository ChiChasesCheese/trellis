---
id: hi-x-reserve-confirm-saga-4-pitfall
node: sd.cross.reserve-confirm-saga
type: qa
step: 4
---
## Q
**先预留再确认与补偿 (Reserve-Confirm / Saga instead of 2PC)**｜跨题模式 · 易错

在"预留—扣款—确认"这类题里，候选人最常犯哪几个错？每个错的具体后果是什么？

## A
1. **把扣款超时当失败，立刻把库存放回。** 钱可能已经扣了；放回去再卖给别人，就是超卖或"收了钱没给货"。正确做法：用同一个幂等键重试，仍不明就停在 PAYING，由对账任务向对方查询后再决定。多占一会儿库存比超卖安全。（[[crowdfunding-share-purchase|限时众筹购股系统]]）
2. **释放预留不幂等。** 过期清扫和用户取消同时到达，同一份库存被释放两次，库存虚增，随后超卖。正确做法：只有状态确实从 HELD 变成 EXPIRED（看条件更新的影响行数）才归还库存。（[[event-ticket-booking|活动票务预订后端]]、[[tt-flash-sale-ticketing|秒杀抢票]]）
3. **把慢的付款调用放进数据库事务。** 事务持有库存行锁等第三方响应，热门票型整体被堵死。正确做法：拆成"保留"和"确认"两个短事务，中间靠状态和幂等键衔接。（[[event-ticket-booking|活动票务预订后端]]）
4. **忽略迟到的成功回调。** 预留已过期并被释放，付款成功的回调才到：钱已收。正确做法：票还在就恢复订单，不在就自动退款。（[[tt-flash-sale-ticketing|秒杀抢票]]、[[hotel-booking-system|酒店预订系统]]）
5. **用户点撤单就释放冻结资金。** 订单可能正在成交，释放后又成交，资金被重复占用。正确做法：等交易所的最终回执，`CANCELED` 才释放，"已成交"就按成交处理。（[[stock-trading-platform|股票交易平台]]）
6. **顺序反了：先扣钱再预留。** 预留失败就得退款，退款又可能失败，补偿链更长更危险。（[[grocery-subscription-orders|生鲜订阅转订单服务]]）
