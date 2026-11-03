---
id: hi-pt-event-ticket-booking-6-sweeper
node: qb.lld.event-ticket-booking.points
type: qa
step: 6
---
## Q
**活动票务预订后端 · 过期释放与幂等保护**｜必会 · 出自：活动票务预订后端 › 深入 3

活动票务的保留超时后要把库存还回去。过期任务和用户购买请求同时到达时，怎样避免同一份库存被释放两次或被错误释放？

## A
**要点。** 每次状态迁移用条件更新并检查影响行数：UPDATE ... WHERE status='HELD'，只有状态确实从 HELD 变成 EXPIRED 才归还 held。
**结果。** 过期任务与购买同时到达，只有一个能改成功，另一个得到明确错误（410 保留过期）。
**体验。** 读可售数时可把过期保留当作已释放，减少用户看到售罄的时间。
