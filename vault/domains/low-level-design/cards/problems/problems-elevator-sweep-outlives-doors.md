---
id: problems-elevator-sweep-outlives-doors
node: problems.machines.elevator
type: qa
step: 2
tags: [grown]
---
## Q
电梯的状态机有 IDLE / MOVING_UP / MOVING_DOWN / DOORS_OPEN 四个状态。如果“这一趟扫描朝哪个方向”只靠这个状态枚举表达，会出什么 bug？

## A
会在每次停靠后丢失方向。开门时状态是 DOORS_OPEN、关门后回到 IDLE，两者都不含方向信息，于是 SCAN 下一拍只能退化成“随便挑一个最近的”，一趟扫描被打断成无数次贪心选择，公平性保证直接消失。正确做法是把“此刻在做什么”（状态枚举）和“这一趟朝哪走”（一个独立的 `sweep: Direction | None` 字段）分开存：`sweep` 跨越开关门保持不变，只有当所有停靠集合都空了才清成 `None`。这条不变式值得专门写一个测试钉住。
