---
id: hi-pt-elevator-design-1-classes
node: qb.lld.elevator-design.points
type: qa
step: 1
---
## Q
**电梯系统 · 类划分与职责**｜出自：电梯系统 › 核心实体与接口

面向对象设计电梯系统，核心类怎么划分？`Elevator`、`Dispatcher`、`Controller` 各自负责什么？用了哪些设计模式？

## A
**要点。** `Elevator` 是小状态机，持有楼层、方向 `Dir`（UP/DOWN/IDLE）、三组待服务集合，提供 `tick()` 和 `eta(floor, dir)`；`Dispatcher` 抽象、`NearestCar` 实现，`pick` 选负责的电梯；`Controller` 是入口：`hall_call`、`cabin_call`、`tick`。
**模式。** 策略（调度）、状态（方向与门）、观察者（楼层显示）。
