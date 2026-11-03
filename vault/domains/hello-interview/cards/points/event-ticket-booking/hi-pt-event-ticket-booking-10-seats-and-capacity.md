---
id: hi-pt-event-ticket-booking-10-seats-and-capacity
node: qb.lld.event-ticket-booking.points
type: qa
step: 10
---
## Q
**活动票务预订后端 · 选座与容量修改**｜加分 · 出自：活动票务预订后端 › 深入 6

活动票务要扩展到选座位，或主办方修改票型数量，设计要怎么调整？

## A
**选座。** 从计数改为逐座位行，保留时对座位行条件更新 WHERE status='AVAILABLE'，检查影响行数等于座位数；固定加锁顺序。
**改容量。** 新 total 不能小于 sold + held；各票型总量之和不超场馆容量，同事务校验。
**价格。** 修改价格不影响已存在的保留与订单。
