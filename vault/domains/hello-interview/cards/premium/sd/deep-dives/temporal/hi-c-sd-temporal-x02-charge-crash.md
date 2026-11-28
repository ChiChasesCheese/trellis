---
id: hi-c-sd-temporal-x02-charge-crash
node: sd.deep-dives.temporal.exam
type: qa
step: 2
---
## Q
**Temporal · 扣款成功但上报前崩溃**｜考点 · 必会

Stripe 已经扣款成功，但执行 `chargeCustomer` Activity 的 worker 在向 Temporal 报告完成之前崩溃了。会发生什么？如何保证不重复扣款？

## A
- **会发生什么：** 历史里没有 `ChargeCustomerCompleted`。Activity 超时（或心跳丢失）后 Temporal 会按重试策略重新调度，另一个 worker 再次调用 Stripe，可能重复扣款。Temporal 保证的是"至少执行一次"，而不是恰好一次。
- **做法：** 让 Activity 幂等。把一个稳定的幂等键（如订单号，或 Workflow ID 加 Activity ID）随请求发给 Stripe（Stripe 支持幂等键），重复请求返回第一次的结果而不是再次扣款。
- **其他外部操作也一样：** 数据库写入用唯一约束或条件更新，发邮件用去重键。
- **记住边界：** 重放保护的是"已记录完成的操作不会重做"；"做了但没来得及记录"的缝隙只能靠幂等关上。
