---
id: amz-robot-restaurant-common-mistake-charger-counter-leak
node: amazon.amz-robot-restaurant
type: qa
step: 9
tags: [grown]
---
## Q
在 Amazon 机器人餐厅设计里，常见错误是给充电桩另设一个 `occupied` 计数器。它会怎样出错？怎么避免？

## A
计数器是第二份真相：机器人状态说「在充电」，计数说「占了几个」，任何一条路径改了状态却忘了释放（比如充电中途被取消），桩就泄漏，最后所有低电量机器人永远等一个不空的桩。避免：占用数 = 处于 CHARGING 的机器人个数，每次现数，机器人离开该状态时占用自然减一，没有可忘记的释放步骤。
