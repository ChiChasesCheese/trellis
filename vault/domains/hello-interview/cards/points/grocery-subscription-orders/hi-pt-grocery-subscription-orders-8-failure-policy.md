---
id: hi-pt-grocery-subscription-orders-8-failure-policy
node: qb.lld.grocery-subscription-orders.points
type: qa
step: 8
---
## Q
**生鲜订阅转订单服务 · 失败后的策略**｜追问 · 出自：生鲜订阅转订单服务 › 逐步扩展 1

余额不足或库存不足时，订阅服务应该怎么办？重试逻辑要不要写进转换代码？

## A
**余额不足。** 三种策略：跳过本期并通知充值；宽限期内每天重试几次；连续几期失败后自动暂停订阅。
**库存不足。** 整单跳过，或对可满足部分发货（需部分扣款，复杂度高）；先实现整单。
**设计。** 失败策略是产品策略，用 `FailurePolicy` 接口承接，不把重试写死在转换代码里；失败结果要可区分，不静默丢失。
