---
id: hi-c-sd-flash-sale-b01-webhook-handling
node: sd.problem-breakdowns.flash-sale.beyond
type: qa
step: 1
---
## Q
**限时抢购 · 拓展：支付 webhook 必须幂等、可验证、可补偿**｜拓展 · 加分

支付方的 webhook 在生产里有哪些要小心的地方？

## A
- **会重复，也可能乱序：** 支付方在你的端点超时或返回错误时会重发，同一事件可能到达多次，不同事件的顺序也不保证。处理要幂等：以事件 ID 去重，状态迁移用条件更新（`WHERE status='PENDING'`），重复到达无副作用。
- **要验签：** 任何人都可以向公开端点发请求。用支付方提供的签名头与共享密钥校验请求体（Stripe 用 `Stripe-Signature`），验证失败直接拒绝，不能凭 payload 里的字段行事。
- **要快速确认：** 端点收到后先落库、立即返回 2xx，耗时处理放到队列里异步做，否则超时会触发重发。
- **可能丢：** webhook 不是 100% 到达。对长时间停留在 PENDING 的购买，用定时任务主动向支付方查询 PaymentIntent 的状态（对账）来补上。
- **和库存的关系：** 支付失败或超时要把预留放回；支付成功与预留已被回收的冲突按"自动退款"兜底。
