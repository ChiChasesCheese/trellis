---
id: amz-robot-restaurant-edge-low-battery-no-free-charger
node: amazon.amz-robot-restaurant
type: qa
step: 7
tags: [grown]
---
## Q
在 Amazon 机器人餐厅设计里，机器人电量低于阈值（低电量线）30、而唯一的充电桩被占着，它该不该接单？电量 25 与 12 的机器人对一碗耗电 8 的汤各自怎样？

## A
接单条件不是「当前是否低于阈值」，而是「做完后电量仍不低于保底电量」：`battery - job_cost >= reserve`（保底 10）。25 − 8 = 17 ≥ 10，可以接，做完剩 17；12 − 8 = 4 < 10，不能接，订单继续排队，机器人原地等桩。若改成「低于阈值就不接单」，没有空桩时订单会无限排队，餐厅停摆。所以再配一条下界：下单时拒绝耗电超过 `low_battery − reserve` 的菜，这样电量不低于阈值的机器人一定能接任何合法订单，系统总有进展，不死锁。
