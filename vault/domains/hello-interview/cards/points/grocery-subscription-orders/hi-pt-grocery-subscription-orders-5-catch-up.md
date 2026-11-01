---
id: hi-pt-grocery-subscription-orders-5-catch-up
node: qb.lld.grocery-subscription-orders.points
type: qa
step: 5
---
## Q
**生鲜订阅转订单服务 · run_due 补跑错过的多期**｜出自：生鲜订阅转订单服务 › 整体设计

任务因停机错过了几个周期，`run_due` 应该怎么处理？下一次执行日期何时推进？

## A
**做法。** `while` 循环对活跃且 `next_run <= today` 的订阅逐期调用 `_convert`，每期用各自的 `cycle` 日期生成订单，并把 `next_run` 推进一个周期。
**要点。** 无论成败都推进 `next_run`，否则同一期会被无限重复尝试；重试由失败策略以单独记录驱动。
