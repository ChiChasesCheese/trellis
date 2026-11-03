---
id: hi-pt-hotel-booking-system-7-state-outbox
node: qb.sd.hotel-booking-system.points
type: qa
step: 7
---
## Q
**酒店预订系统 · 状态机加发件箱恢复**｜追问 · 出自：酒店预订系统 › 深入 5

预订过程中支付或供应商不可用甚至宕机，怎么不丢单、不超卖、不重复扣款？为什么不用两阶段提交？

## A
**状态机。** HELD → PAID → PENDING_SUPPLIER → CONFIRMED；每步在本地事务内改状态，并写一条待发消息到发件箱（outbox），由中继投递，保证状态变更与外部调用不会只成功一半。
**幂等。** 调供应商用预订 ID 作幂等键；超时进重试队列，用户看到「确认中」。
**补偿。** 供应商最终拒绝则释放库存并退款；对账任务定期修复不一致。
