---
id: hi-ov-ticketmaster-2-options
node: sd.problem-breakdowns.ticketmaster
type: qa
step: 2
tags: [通览]
---
## Q
**票务预订（Ticketmaster） · 高层设计**｜通览

票务预订的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** 客户端、API 网关、活动服务、搜索服务、订票服务、Events DB、支付处理方 Stripe。

**每条路径。**
- **查看活动：** 请求经网关到活动服务，读 Events DB 的活动、场馆、表演者和座位，返回座位图。
- **搜索活动：** 请求经网关到搜索服务，按关键词、日期等参数过滤 Events DB。
- **订票：** 请求到订票服务，在一个事务里检查票可用、改为已订、写 Booking；Stripe 处理付款；票已被抢则失败返回。

**存储。** 活动、票、订单放同一个 PostgreSQL；订票需要事务来保证不重复卖，且这些数据紧密关联。
