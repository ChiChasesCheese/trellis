---
id: hi-lld-elevator-4-request-class
node: lld.problem-breakdowns.elevator.exam
type: qa
step: 4
---
## Q
**请求存什么：纯楼层号还是 Request 类**｜低层设计 · 题目拆解

Elevator 内部的待停集合，用 `Set<int>` 存楼层号可以吗？要不要引入带类型的 Request 类？

## A
**要点。** 引入 `Request(floor, type)`，`type` 取 PICKUP_UP、PICKUP_DOWN、DESTINATION 三种；`equals` 和 `hashCode` 同时比较楼层与类型，所以 (7, 上)、(7, 下)、(7, 目的) 是三个不同请求。

**为什么。** 只存楼层号时，电梯在 5 层上行、7 层有人按了「下」，集合里 7 已存在，没有任何记录。电梯上行到 7 层停下，等下行的人上了一部上行的车，被带到 8 层再折返。带类型后，上行经过 7 层时只找 (7, 上) 和 (7, 目的)，找不到就不停，折返下行时才命中 (7, 下)。

**取舍。** 代价是多一个类和 `equals/hashCode`，对初级面试可以省略。

**易错。** 方向要有 IDLE 状态，否则没有请求时电梯没法表示「不动」，会一直漂移。
