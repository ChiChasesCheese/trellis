---
id: hi-pt-payment-batch-processing-5-two-layer-idem
node: qb.sd.payment-batch-processing.points
type: qa
step: 5
---
## Q
**支付处理系统（授权冻结加每日批量结算） · 两层幂等**｜出自：支付处理系统（授权冻结加每日批量结算） › 深入 1

支付处理器怎样保证重复请求绝不重复扣款？

## A
**商户到我们。** (merchantId, Idempotency-Key) 唯一约束，存请求体哈希与响应；同键同体返回原响应，同键不同体返回 422，并发的后到者见 IN_PROGRESS 返回 409。
**我们到网络。** 用 holdId / chargeId 作网络侧引用号，我们自己的重试不会产生第二笔冻结。
**两层缺一不可。** 第一层防商户重发，第二层防我们重试。
