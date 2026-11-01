---
id: hi-pt-tt-payment-reconciliation-10-paid-not-booked
node: tt.sd.tt-payment-reconciliation.points
type: qa
step: 10
---
## Q
**支付对账系统 · 渠道已扣款订单未支付**｜出自：支付对账系统 › 深入 3

对账发现某笔款项渠道已扣但订单仍是未支付，怎么处理？

## A
**性质。** 这是账本缺失里最危险的一种：PSP 有、我们没有。
**做法。** 先向 PSP 查询确认，再补入账并通知订单继续履约；订单已取消则自动退款。
**边界。** 能安全自动修复的才自动，涉及退款的人工复核。
**上游反馈。** 账本缺失增多说明回调或轮询出了问题，要回流上游。
