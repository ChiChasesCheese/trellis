---
id: hi-c-sd-temporal-n01-problem
node: sd.deep-dives.temporal.notes
type: qa
step: 1
---
## Q
**Temporal · 它要解决什么问题**｜摘要 · 必会

一个"扣款、占库存、发货、等几天收货、发评价邮件"的订单流程，直接写成顺序函数为什么不行？

## A
- **理想写法：** 顺序调用 `chargeCustomer`、`reserveInventory`、`requestShipment`，循环等待"已送达"，再 `sendReviewEmail`。
- **问题一，等待：** 不可能让一个进程为每个订单睡 5 天。得把流程拆开，把当前状态存到某处，等承运商通知后再触发下一步。
- **问题二，中途崩溃：** Stripe 已扣款成功，服务器恰好崩溃。接手的服务器怎么知道扣过款？重跑这一步可能重复扣款。
- **自己造基础设施很难做对：** 这类需要持久化执行（durable execution）的问题，正是 Temporal 要处理的。其他办法还有用事件协调服务、或 AWS Step Functions 这类工作流系统。
