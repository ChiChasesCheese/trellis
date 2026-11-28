---
id: hi-c-sd-ticketmaster-n11-booking-flow
node: sd.problem-breakdowns.ticketmaster.notes
type: qa
step: 11
---
## Q
**票务系统 · 完整订票流程与支付 Webhook**｜摘要 · 必会

从选座到付款成功的完整步骤是什么？为什么客户端用 Stripe.js，Webhook 为什么要幂等？

## A
- **选座：** 客户端 `POST /bookings` 带 ticketId，经网关到订票服务；服务用 Redis 加锁，TTL 10 分钟；同时在数据库写一条状态为 in-progress 的订单；返回 bookingId，客户端跳到结账页。
- **用户放弃：** 10 分钟后锁自动释放，票可再被订。
- **支付：** 客户端用 Stripe.js 把卡信息令牌化，服务端从不接触原始卡号（PCI 合规的标准做法）；把令牌和 bookingId 发给服务端，服务端创建 Stripe PaymentIntent；Stripe 处理后通过 Webhook 通知。
- **确认：** Webhook 从元数据取出 bookingId，开一个数据库事务，同时把票改为 booked、订单改为 confirmed。
- **幂等：** Stripe 失败时会重试 Webhook，同一事件处理两次不能产生重复状态变化。以 bookingId 作幂等键，更新前检查订单当前状态，重试就安全了。
