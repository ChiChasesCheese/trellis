---
id: method-invariant-ownership
node: method.modeling
type: qa
step: 3
---
## Q
需求是"一个车位最多停一辆车"，应该由哪个类来执行这条规则——为什么不是调用它的 `ParkingService`？

## A
应该由状态的所有者来执行：`Spot.park(vehicle)` 在车位已被占用时直接拒绝。如果放在 service 里执行，就意味着现在和将来任何一条调用路径都可能绕过检查去破坏这个车位——这条不变式就只是靠约定维持，而不是被强制保证。

原则：实体保护自己的不变式，service 只负责编排。把校验放在数据的所有者身上，非法状态就从任何调用方那里都到达不了。
