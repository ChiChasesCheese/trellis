---
id: hi-c-sd-payment-system-n04-api
node: sd.problem-breakdowns.payment-system.notes
type: qa
step: 4
---
## Q
**支付系统 · 接口设计**｜摘要 · 必会

支付系统的三个核心接口怎么设计？卡号为什么不能这样直接传，Webhook 又是什么？

## A
- **创建意图：** `POST /payment-intents`，体含 `amountInCents`（整数分）、`currency`、`description`，返回 `paymentIntentId`。在顾客到商户结账页时调用。
- **支付：** `POST /payment-intents/{id}/transactions`，体含 `type: charge` 和卡信息。真实系统里绝不会把卡号原样传给后端，要用安全的令牌化；面试里只要说明你知道这些数据必须加密。
- **查状态：** `GET /payment-intents/{id}`，返回当前状态（pending、succeeded、failed）和失败时的错误信息。
- **Webhook（更贴近业界）：** 商户给我们一个回调地址，状态变化时我们向它 POST 事件，如 `payment.succeeded`，让商户实时获知。
- **范围提醒：** 设计 Webhook 系统本身就是一道完整的面试题，同时做支付加 Webhook 在时限内太多，要在开头和面试官对齐。
