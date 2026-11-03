---
id: hi-pt-tt-merchant-webhook-delivery-2-at-least-once
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 3
---
## Q
**商户回调（Webhook）投递系统 · 只能至少一次**｜必会 · 出自：商户回调（Webhook）投递系统 › 深入 1

能做到恰好一次吗？为什么？平台和商户各自承担什么？

## A
**不能。** 工人收到 200 之后、写库之前崩溃，或商户处理了但响应在网络上丢了，都存在「商户处理了而平台不知道」的窗口，是外部系统的本质。
**做法。** 至少一次：同一事件每次重试用同一个 `X-Event-Id`，商户按事件号去重、先落库后响应。
**唯一键。** 平台一侧的 `(event_id, endpoint_id)` 只保证扇出不重复。
