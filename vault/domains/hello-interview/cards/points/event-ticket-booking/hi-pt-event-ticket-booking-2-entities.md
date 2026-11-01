---
id: hi-pt-event-ticket-booking-2-entities
node: qb.lld.event-ticket-booking.points
type: qa
step: 2
---
## Q
**活动票务预订后端 · 票型与保留实体**｜出自：活动票务预订后端 › 核心实体与接口

活动票务后端的数据模型怎么建，才能直接算出可售数量并追踪保留的生命周期？

## A
**票型。** TicketType 存 total、sold、held、price_cents、sale_start、sale_end，可售数 = total − sold − held。
**保留。** Reservation 状态 HELD → CONFIRMED / EXPIRED / CANCELLED，带 qty、expires_at、idempotency_key。
**订单。** Booking 含 payment_status（PENDING、PAID、FAILED、REFUNDED），另有 Refund 记录。
**价格。** 订单保存下单时的价格快照。
