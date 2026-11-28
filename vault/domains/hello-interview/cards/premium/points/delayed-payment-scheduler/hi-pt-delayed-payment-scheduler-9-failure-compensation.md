---
id: hi-pt-delayed-payment-scheduler-9-failure-compensation
node: qb.sd.delayed-payment-scheduler.points
type: qa
step: 9
---
## Q
**延迟支付调度服务 · 失败重试与补偿**｜追问 · 出自：延迟支付调度服务 › 深入 5

到点入账失败了：可能是暂时故障，也可能是收款账户已被封。分别怎么处理？

## A
**暂时性失败。** 指数退避，把 `lease_until` 推到未来，最多约 10 次。

**永久性失败。** 收款账户被封或注销时，写 REFUND 分录退回付款人，状态 FAILED，通知付款人。

**兜底。** 重试耗尽进入人工队列，不静默丢弃。
