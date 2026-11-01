---
id: hi-pt-payment-batch-processing-3-write-intent-first
node: qb.sd.payment-batch-processing.points
type: qa
step: 3
---
## Q
**支付处理系统（授权冻结加每日批量结算） · 先写意图再调外部**｜出自：支付处理系统（授权冻结加每日批量结算） › 整体设计

支付处理器收到冻结请求，应该先调外部支付网络，还是先写数据库？

## A
**要点。** 先写 PENDING 的 hold（同时登记 Idempotency-Key 唯一约束），再调网络。
**为什么。** 先调网络再写库，崩溃时会有钱冻了但我们不知道的交易，没有记录可恢复；先写库最坏是有一行 PENDING 而网络没收到，恢复任务可安全处理。
