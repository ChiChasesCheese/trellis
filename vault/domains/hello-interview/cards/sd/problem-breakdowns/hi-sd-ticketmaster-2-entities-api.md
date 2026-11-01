---
id: hi-sd-ticketmaster-2-entities-api
node: sd.problem-breakdowns.ticketmaster
type: qa
step: 2
---
## Q
**核心实体与 API 的演进**｜系统设计 · 问题拆解

票务系统有哪些核心实体？Ticket 与 Booking 为什么分开？订票接口一开始怎么设计，之后会如何演化？

## A
**实体。** Event（日期、描述、类型）、User、Performer（艺人 / 球队 / 团体，故意取得宽泛）、Venue（地址、容量、座位图）、Ticket（活动、座位、价格、可售状态）、Booking。

**Ticket 与座位图。** 创建活动时，按场馆座位图为每个座位生成一张票；座位图存于 Venue（如 JSON），客户端用它加每张票的状态渲染选座界面。

**Booking。** 可以并入 Ticket，但一次买多张票时，单独的订单实体能把它们归到同一笔订单、共享支付状态和总价。

**接口。**
- `GET /events/:eventId` 返回活动、场馆、艺人和票列表
- `GET /events/search?keyword&start&end&pageSize&page`
- `POST /bookings/:eventId`，带 ticketIds 与支付信息，返回 bookingId

**演化。** 先给最简接口，并声明之后会拆成「预订」与「确认购买」两个接口。
