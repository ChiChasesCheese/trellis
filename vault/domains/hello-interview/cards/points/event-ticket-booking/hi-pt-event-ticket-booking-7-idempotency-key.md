---
id: hi-pt-event-ticket-booking-7-idempotency-key
node: qb.lld.event-ticket-booking.points
type: qa
step: 7
---
## Q
**活动票务预订后端 · 幂等键与错误码**｜出自：活动票务预订后端 › 深入 4

活动票务接口里，客户端网络超时后重试保留请求，如何避免重复占库存？接口还应返回哪些清晰错误码？

## A
**幂等。** 请求头 Idempotency-Key，数据库对 (user_id, idempotency_key) 加唯一约束，同一键返回同一保留。
**错误码。** 409 售罄、410 保留过期、422 未开售、429 限流。
**付款失败。** 保留仍有效，用户可换卡重试。
