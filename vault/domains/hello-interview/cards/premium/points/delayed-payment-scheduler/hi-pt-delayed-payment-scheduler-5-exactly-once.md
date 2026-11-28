---
id: hi-pt-delayed-payment-scheduler-5-exactly-once
node: qb.sd.delayed-payment-scheduler.points
type: qa
step: 5
---
## Q
**延迟支付调度服务 · 恰好一次转账**｜必会 · 出自：延迟支付调度服务 › 深入 2

到点执行时要给收款人加钱，收款人可能在另一个数据库分片。怎样保证不重复、不丢失，又不用分布式事务？

## A
**要点。** 至少一次加幂等。创建时已预留，执行只剩一个跨分片动作：给收款人入账，对 `(holdId, CREDIT)`（预留编号加分录类型）加唯一约束，重复插入失败就视为已入账。

**顺序。** 先入账，后把预约标记为 COMPLETED。反过来，标记完成后崩溃，钱就丢了。
