---
id: hi-lld-elevator-5-no-interface
node: lld.problem-breakdowns.elevator.exam
type: qa
step: 5
---
## Q
**别抽象 IRequestHandler**｜低层设计 · 题目拆解

ElevatorController.requestElevator 和 Elevator.addRequest 看起来都是「加请求」，是否应该抽出共同接口？

## A
**要点。** 不该。两者做的事本质不同：`requestElevator` 是协调操作，要在多部电梯里选一部；`addRequest` 只是对单部电梯的状态修改。

**为什么。** 接口的价值在于多态：同一行为有多个可互换的实现。控制器不是一种电梯，两者也无法互相替换，参数相似不代表抽象相同。硬抽只会增加理解成本。

**取舍。** 真正适合抽象的地方是「选哪部电梯」：如果不同楼宇要不同调度目标（最短等待、最省电），把 `selectBestElevator(request)` 做成可替换的策略（Strategy pattern）。

**易错。** 面试里「为了显得会设计模式」而加接口，是扣分项；能说清为什么不加，反而是加分项。
