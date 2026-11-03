---
id: hi-pt-beverage-vending-system-6-menu-select
node: qb.lld.beverage-vending-system.points
type: qa
step: 5
---
## Q
**多地点饮品自助售卖系统 · 菜单推导与选机策略**｜追问 · 出自：多地点饮品自助售卖系统 › 逐步扩展 1

菜单是单独维护还是由库存推导？为什么下单时还要以 `reserve` 为准？机器选择规则怎么留出变化空间？

## A
**菜单。** 由库存推导（`can_make`），避免「菜单上有、实际做不了」。
**为什么。** 展示菜单和下单之间库存可能变化，所以以 `reserve` 结果为准。
**选机。** 抽成 `MachineSelector` 策略接口：最近优先、库存最充裕、排队最短，运行时可换。
