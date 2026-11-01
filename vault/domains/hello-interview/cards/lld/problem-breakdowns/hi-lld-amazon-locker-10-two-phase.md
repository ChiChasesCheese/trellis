---
id: hi-lld-amazon-locker-10-two-phase
node: lld.problem-breakdowns.amazon-locker
type: qa
step: 10
---
## Q
**扩展：确认包裹真的放进去了**｜低层设计 · 题目拆解

快递柜现在是开门后立刻生成取件码，如果快递员开了门又没放包裹就走了，就会出现对应空格口的码。怎样改成保证包裹已存入？代价是什么？

## A
**做法。** 把存件拆成两阶段（two-phase）：

- `reserve_compartment(size)`：找格口，标为已预留（RESERVED），开门，返回预约号
- 快递员放入包裹后调用 `confirm_deposit(reservation_id)`：标为占用，生成取件码并存表，删除预约
- `cancel_reservation(reservation_id)`：放弃时释放

格口状态增加 RESERVED；Locker 另维护预约号到格口的映射。预约要有超时（比如 2 到 3 分钟没确认就自动取消并释放），避免格口被卡住。

**取舍。** 复杂度明显增加：多一个状态、一张映射表和超时逻辑。面试范围内，单阶段的方案更干净、够用；生产环境如果必须保证包裹在位，才需要两阶段加传感器或人工确认。
