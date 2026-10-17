---
id: amz-robot-restaurant-robot-state-machine-transition-table
node: amazon.amz-robot-restaurant
type: qa
step: 4
tags: [grown]
---
## Q
在 Amazon 机器人餐厅设计里，机器人的状态机有哪些状态、哪些转移合法？这些规则放在哪里？

## A
状态：IDLE、COOKING、DELIVERING、CHARGING。合法转移只有 IDLE→COOKING、IDLE→CHARGING、COOKING→DELIVERING、DELIVERING→IDLE、CHARGING→IDLE，写成一张字典 `_ALLOWED`，唯一改状态的方法 `_to(new)` 查表，不在表里就抛 `InvalidTransitionError`。所以做菜中的机器人不可能被直接派去充电。四个状态用枚举加表就够，不必拆成四个状态类。
