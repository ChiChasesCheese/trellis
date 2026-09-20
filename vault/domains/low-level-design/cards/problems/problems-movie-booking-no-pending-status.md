---
id: problems-movie-booking-no-pending-status
node: problems.booking.movie-booking
type: qa
step: 7
tags: [grown]
---
## Q
电影订票设计里，订单状态要不要设 PENDING（已选座、未付款）这一档，即选座时先建一张 PENDING 订单、付款后改成 CONFIRMED？

## A
不要。"已选座、未付款"这件事已经由带超时的**锁座收据**（seat hold）完整表达了：它有座位、有用户、有过期时间、有清扫规则。再建一张 PENDING 订单就是同一件事的第二份表示，两者都要过期、都要被清扫、而且必须始终一致——第一个 bug 一定是"收据过期了但 PENDING 订单还留着"。所以订单只需要 CONFIRMED 和 CANCELLED 两个状态，订单只在付款成功后才诞生。一般规律：一个状态只在一个地方表达，是这类设计题最省事的纪律；看到两个对象同时描述同一件事的生命周期，就该合并掉一个。
