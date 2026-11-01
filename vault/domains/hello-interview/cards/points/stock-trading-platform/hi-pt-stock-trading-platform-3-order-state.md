---
id: hi-pt-stock-trading-platform-3-order-state
node: qb.sd.stock-trading-platform.points
type: qa
step: 3
---
## Q
**股票交易平台（券商端） · 订单状态机**｜出自：股票交易平台（券商端） › 核心实体与接口

限价单的订单状态包含哪些？合法的转换有哪些？接口怎么保证不重复下单？

## A
**状态。** `NEW → SENT → ACKED → PARTIALLY_FILLED → FILLED`；或 `→ CANCEL_REQUESTED → CANCELED`；或 `→ REJECTED / EXPIRED`。
**规则。** 只允许合法转换，例如 FILLED 不能再变成 CANCELED，非法转换丢弃并记日志。
**幂等。** `POST /orders` 带 `Idempotency-Key`，`clientRequestId` 有唯一约束；`DELETE` 返回"已请求取消"，最终结果异步。
