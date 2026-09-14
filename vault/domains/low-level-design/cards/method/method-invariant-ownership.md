---
id: method-invariant-ownership
node: method.modeling
type: qa
---
## Q
Requirement: "a spot holds at most one vehicle." Which class enforces this invariant — and why not the `ParkingService` that calls it?

## A
The owner of the state: `Spot.park(vehicle)` fails if already occupied. Enforcing it in the service means every current and future call path can corrupt the spot — the invariant holds only by convention.

Rule: **entities protect their own invariants; services orchestrate**. Enforcement at the data owner makes the illegal state unreachable from any caller.


## Q zh
需求："一个位置最多持有一辆车。"哪个类执行这个不变式 — 为什么不是调用它的 `ParkingService`?

## A zh
状态的所有者: `Spot.park(vehicle)` 如果已被占用则失败。在服务中执行它意味着每个现在和未来的调用路径都能腐蚀位置 — 不变式只按约定保持。

规则: **实体保护它们自己的不变式；服务编排**。在数据所有者处执行使得非法状态从任何调用者处不可达。
