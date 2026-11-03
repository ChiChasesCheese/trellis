---
id: hi-pt-payment-batch-processing-4-unknown-timeout
node: qb.sd.payment-batch-processing.points
type: qa
step: 5
---
## Q
**支付处理系统（授权冻结加每日批量结算） · 未知不等于失败**｜必会 · 出自：支付处理系统（授权冻结加每日批量结算） › 深入 1

支付处理器调用网络超过 3 秒没应答，不知道额度冻住没有。怎么处理？按失败类型各自的重试规则是什么？

## A
**超时。** 状态记 UNKNOWN，异步恢复任务按引用号查询；查不到或不支持查询就发冲正（reversal，幂等）。绝不换通道重新发起，否则可能冻两次。
**明确被拒。** 业务终态，不重试。
**明确失败。** 连接建立前就断，安全重试。
**商户侧。** 先返回失败请重试，新 Idempotency-Key 不与未知交易冲突。
