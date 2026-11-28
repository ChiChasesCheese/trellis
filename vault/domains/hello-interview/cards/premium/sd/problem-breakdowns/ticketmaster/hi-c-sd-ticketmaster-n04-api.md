---
id: hi-c-sd-ticketmaster-n04-api
node: sd.problem-breakdowns.ticketmaster.notes
type: qa
step: 4
---
## Q
**票务系统 · 接口设计**｜摘要 · 必会

查看、搜索、订票三个接口怎么设计？为什么订票接口之后会演进？

## A
- **查看：** `GET /events/:eventId` 返回活动、场馆、表演者和票列表（票用来在客户端渲染座位图）。
- **搜索：** `GET /events/search?keyword&start&end&pageSize&page`，返回匹配的活动列表。
- **订票：** `POST /bookings/:eventId`，体里是 `ticketIds` 和支付信息，返回 `bookingId`。
- **演进：** 之后会拆成两个接口：预留座位（占座）和确认购买（付款）。先给最简接口，并说明「设计深入后会演进」是可以的。
- **别写太细：** 面试官能从实体和需求看出返回什么，枚举 Event 的每个字段浪费时间。
