---
id: hi-pt-payment-batch-processing-8-single-leader
node: qb.sd.payment-batch-processing.points
type: qa
step: 8
---
## Q
**支付处理系统（授权冻结加每日批量结算） · 批处理单领导者**｜追问 · 出自：支付处理系统（授权冻结加每日批量结算） › 深入 4

支付处理器的批处理调度器如果两个实例同时运行，会重复生成同一批。怎么避免？

## A
**要点。** 调度器必须单领导者：租约加围栏令牌（fencing token），避免旧领导者的过期写入。
**工作流。** 用 Temporal 一类工作流引擎，进程崩溃后从断点继续。
**对账。** 我们账本应收、网络结算报告、银行实际到账三方比对，差异进人工队列。
