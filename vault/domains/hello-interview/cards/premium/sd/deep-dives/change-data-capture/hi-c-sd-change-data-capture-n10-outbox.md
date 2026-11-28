---
id: hi-c-sd-change-data-capture-n10-outbox
node: sd.deep-dives.change-data-capture.notes
type: qa
step: 10
---
## Q
**变更数据捕获 · 事务发件箱（outbox）**｜摘要 · 必会

如何让应用显式地记下「订单已发货」这个业务事件，并保证它和订单状态一致？

## A
- **做法：** 应用在更新订单的同一个事务里，向 `outbox_events` 表插入一行，包含 `event_id`、`event_type`（如 OrderShipped）、`payload`。
- **原子性：** 两行要么一起提交，要么都不提交，所以只有订单真的发货了才会有这行事件。
- **转发：** 一个中继（relay）读取发件箱表的事件并发布给下游。
- **关键区别：** `orders.status` 是应用状态；发件箱行是因为应用判定业务事件发生才写的，带有稳定的 `event_id`，下游可以拿来去重。
- **契约：** 下游依赖发件箱事件，而不是 orders 表的变化。
