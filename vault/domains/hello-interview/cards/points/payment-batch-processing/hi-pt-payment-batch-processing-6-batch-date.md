---
id: hi-pt-payment-batch-processing-6-batch-date
node: qb.sd.payment-batch-processing.points
type: qa
step: 6
---
## Q
**支付处理系统（授权冻结加每日批量结算） · 扣款的批次归属**｜出自：支付处理系统（授权冻结加每日批量结算） › 整体设计

支付处理器每晚 10 点是网络的截止时间，扣款请求在截止时刻前后到达。怎么确定它属于哪一批，避免切换时刻竞争？

## A
**要点。** batchDate 由 createdAt 确定性算出：晚上 10 点前归当天，之后归次日。
**为什么。** 它只是 createdAt 的函数，不需要当前批次指针，没有切换时刻的竞争。
**配合。** 截止后再等宽限（如 30 秒）让在途写入落地，按 (network, batchDate) 分区读 RECEIVED 的扣款。
