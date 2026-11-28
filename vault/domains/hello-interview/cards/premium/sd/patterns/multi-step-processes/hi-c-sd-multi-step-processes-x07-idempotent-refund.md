---
id: hi-c-sd-multi-step-processes-x07-idempotent-refund
node: sd.patterns.multi-step-processes.exam
type: qa
step: 7
---
## Q
**多步流程 · 退款为什么会被退两次**｜考点 · 必会

退款 Activity 调支付服务成功了，但在向引擎汇报前 worker 崩溃了。会发生什么，怎么设计？

## A
- **发生什么：** 引擎不知道成功，按策略重试，客户被退两次。引擎保证的是尝试至少一次，不是效果一次。
- **设计：** 给这次退款一个稳定的幂等键（如订单号 + 步骤名），动作前先写 IN_PROGRESS，完成后改 COMPLETED；重试时见 COMPLETED 直接跳过。
- **残留窗口：** 动作完成、写 COMPLETED 之前崩溃，重试会看到 IN_PROGRESS，这时不要盲目重发，转入对账（向支付服务查询这个键对应的退款是否存在）。
- **更好：** 把幂等键一并传给下游支付服务，让对方去重。
- **说法：** 尝试至少一次，靠幂等让效果恰好一次。
