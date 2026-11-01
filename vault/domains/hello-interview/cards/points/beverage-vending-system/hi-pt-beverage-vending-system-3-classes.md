---
id: hi-pt-beverage-vending-system-3-classes
node: qb.lld.beverage-vending-system.points
type: qa
step: 3
---
## Q
**多地点饮品自助售卖系统 · 核心类与职责**｜出自：多地点饮品自助售卖系统 › 核心实体与接口

饮品售卖系统的核心类有哪些？`Recipe`、`Inventory`、`Machine`、`Order`、`OrderService` 各自负责什么？线程安全归谁？

## A
**要点。** `Recipe` 不可变，原料到用量的映射；`Inventory` 管实际量/已预留量，提供 `reserve`、`commit`、`release`、`low_items`，线程安全是它的责任；`Machine` 持有地点、状态、库存、制作队列，经 `MachineController` 驱动硬件；`Order` 是状态机；`OrderService` 选机器、预留、建单、推动状态。
