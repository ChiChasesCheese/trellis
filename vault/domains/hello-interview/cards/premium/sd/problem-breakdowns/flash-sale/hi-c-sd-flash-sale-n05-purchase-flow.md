---
id: hi-c-sd-flash-sale-n05-purchase-flow
node: sd.problem-breakdowns.flash-sale.notes
type: qa
step: 5
---
## Q
**限时抢购 · 高层设计：付款与结果通知**｜摘要 · 必会

购买流程怎么走？为什么用 webhook，客户端怎么知道自己买到没有？

## A
- **流程：** `POST /reservations/:id/purchases` → 服务确认预留存在且未过期 → 建 status=PENDING 的 Purchase → 向 Stripe 一类支付方创建 PaymentIntent，把 client secret 返回客户端 → 客户端**直接**向支付方提交支付信息并确认（我们不碰敏感支付数据）→ 支付方发 webhook 通知结果。
- **webhook：** 一个系统在事件发生时向另一个系统的端点发 HTTP 请求。我们不必反复询问支付状态，终态时对方来通知。成功则 Purchase 标 COMPLETE、Reservation 标 PURCHASED；失败则 Purchase 标 FAILED，预留保持有效直到过期，用户可重试。
- **用户怎么知道：** 支付方告诉了客户端，但我们这边的记录要等 webhook 才落地。最简单：客户端每秒左右轮询 `GET /purchases/:id` 直到终态。只有持有预留的几千人在轮询（不是几千万），成本几乎为零；也可用 SSE 推。
- **模式。** 实时更新：等待者很少、等待只有几秒，轮询比常驻连接更划算；人多或等得久才值得推送。
