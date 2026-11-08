---
id: hi-sd-ticketmaster-7-redis-challenges
node: sd.problem-breakdowns.ticketmaster.exam
type: qa
step: 7
---
## Q
**Redis 锁方案的三个难点与完整订票流程**｜系统设计 · 问题拆解

Redis 锁方案在座位图显示、Redis 故障、支付中 TTL 过期上分别有什么问题？Stripe 付款后怎么确认订单？

## A
**座位图显示。** 预留在 Redis，活动服务要把预留座位显示为不可选。用普通集合会有幽灵条目（成员不会随锁过期），应使用有序集合，以锁的到期时间为分数（`ZADD event:{id}:reserved <expiresAt> ticketId`），读时只统计分数在未来的，并用 `ZREMRANGEBYSCORE` 惰性清理。也可以加锁时把 reserved 写通到数据库。

**Redis 故障。** 体验降级，但不会双订，因为数据库 OCC 兜底；用户可能填完支付才失败。仍好过 cron 失败时所有票都显示不可用。

**支付期间 TTL 到期。** 数据库事务只会让一人成功，另一人自动退款；TTL 设宽裕，支付发起时延长锁。

**流程。** 选座后加锁、写 in-progress 订单、跳支付页；前端用 Stripe.js 令牌化卡号，服务端不碰卡号；Stripe 的 webhook 触发数据库事务，票改 booked、订单改 confirmed。处理器必须幂等（bookingId 作幂等键，先查状态再更新）。
