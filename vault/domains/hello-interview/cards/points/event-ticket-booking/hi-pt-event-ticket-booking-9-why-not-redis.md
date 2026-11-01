---
id: hi-pt-event-ticket-booking-9-why-not-redis
node: qb.lld.event-ticket-booking.points
type: qa
step: 9
---
## Q
**活动票务预订后端 · 库存为什么不只放 Redis**｜出自：活动票务预订后端 › 取舍与追问

面试官问：活动票务的库存计数为什么不直接放 Redis，毕竟计数很快？

## A
**理由。** 库存与订单要同事务一致，Redis 和数据库之间会出现不一致。
**折中。** Redis 只做前置快速拒绝（明显售罄时直接返回），最终以数据库为准。
**对照。** 类的分工：BookingService 编排，TicketType 封装原子方法，PaymentGateway 可替换为假实现注入失败，便于测试。
