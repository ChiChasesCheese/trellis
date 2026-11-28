---
id: hi-c-lld-parking-lot-n05-lot-class
node: lld.problem-breakdowns.parking-lot.notes
type: qa
step: 5
---
## Q
**停车场 · `ParkingLot` 的状态与方法**｜摘要 · 必会

停车场类要记住什么、对外暴露什么？为什么费率放在它里面？

## A
- **状态：** 全部车位；占用集合（哪些车位被占）；活跃票；小时费率。
- **费率放在 Lot：** 定价是系统级策略，不同停车场费率不同，放在构造参数里可建多个实例、也好测试；放全局常量难测，每次出场都传费率则让调用者知道了定价。
- **方法只有两个：** `enter(vehicle) -> Ticket`，没有位置就抛错；`exit(ticket_id) -> 费用（分）`，票无效就抛错。
- **不要加查询方法：** 没有需求要求查询状态时，`get_available_spots()` 之类只会破坏封装；面试官问到监控、看板再加。
- **构造：** 车位列表由外部配置传入，加费率。
