---
id: hi-pt-tt-merchant-webhook-delivery-3-outbox-fanout
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 3
---
## Q
**商户回调（Webhook）投递系统 · 发件箱与扇出**｜出自：商户回调（Webhook）投递系统 › 整体设计

怎样保证「状态变了而事件没发」不可能出现？事件怎样变成对每个端点的投递？

## A
**发件箱。** 支付服务在更新支付状态的同一事务里写 Event。
**扇出。** 扇出服务按订阅查 Endpoint，为每个端点写一行 Delivery，`(event_id, endpoint_id)` 唯一，崩溃重放不产生重复行；任务入队按 `endpoint_id` 哈希分区，便于限制并发。
