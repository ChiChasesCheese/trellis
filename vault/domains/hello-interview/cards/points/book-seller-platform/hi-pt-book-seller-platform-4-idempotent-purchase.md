---
id: hi-pt-book-seller-platform-4-idempotent-purchase
node: qb.sd.book-seller-platform.points
type: qa
step: 4
---
## Q
**图书比价代购平台 · 超时与幂等购买**｜出自：图书比价代购平台 › 深入 2

图书平台向书商发出 purchase 请求后超时，不知道书商到底有没有下单。盲目重试可能买两本，盲目放弃可能顾客被扣钱却没货。应该怎么处理？

## A
**要点。** 每次尝试带稳定的 orderRef（订单号加尝试序号），要求书商的 purchase 按它幂等。
**超时不算失败。** 进入 UNKNOWN 状态，用 status(orderRef) 查询确认；查到才决定成败，查不到再用同一个 orderRef 安全重试。
**并发。** 同一订单同一时刻只让一个编排器处理（行级版本号，或按 orderId 分区的队列）。
