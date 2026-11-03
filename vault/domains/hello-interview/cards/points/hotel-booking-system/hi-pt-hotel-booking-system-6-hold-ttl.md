---
id: hi-pt-hotel-booking-system-6-hold-ttl
node: qb.sd.hotel-booking-system.points
type: qa
step: 5
---
## Q
**酒店预订系统 · 保留 TTL 与支付两阶段**｜必会 · 出自：酒店预订系统 › 深入 3

先保留库存、后支付，怎么防库存被占着不成交？支付回调迟到怎么办？

## A
**保留。** 保留 10 分钟，状态 HELD；支付成功转 CONFIRMED。
**清理。** 定时任务每 30 秒扫 `HELD` 且 `hold_expires_at < now()` 的预订，改 EXPIRED 并把库存减一，同一事务。
**迟到。** 预订已过期则重新尝试扣减，成功就确认，失败就退款。
**支付。** 预授权加扣款，避免钱扣了房没订上。
