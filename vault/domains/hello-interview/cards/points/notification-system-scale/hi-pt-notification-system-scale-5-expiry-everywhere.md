---
id: hi-pt-notification-system-scale-5-expiry-everywhere
node: qb.sd.notification-system-scale.points
type: qa
step: 5
---
## Q
**百万级通知系统 · 每个环节检查过期**｜出自：百万级通知系统 › 深入 3

通知系统的促销过期后不能再发。只在入口检查过期时间够吗？

## A
**不够。** 促销排了 10 分钟队，若不再检查，会发出过期优惠。
**做法。** 消息带 expires_at：流水线出队后检查一次，渠道网关发送前再检查一次，过期的丢弃并记 EXPIRED。
**实现。** 队列里的消息不能原地删除，所以是消费时丢弃；积压深时丢弃只是一次读取，远低于发送成本。
