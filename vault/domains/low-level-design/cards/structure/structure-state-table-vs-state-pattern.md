---
id: structure-state-table-vs-state-pattern
node: structure.state-machines
type: qa
---
## Q
Transition table/enum vs the GoF State pattern (one class per state) — how do you choose in a timed machine-coding round?

## A
Decide by **where the complexity is**:

- **Table/enum** when the logic *is* the transitions and per-state behavior is trivial (order lifecycle, booking status). Far less code — the right default under time pressure.
- **State pattern** when each state carries **substantial distinct behavior** (elevator: MovingUp/DoorOpen/Idle each handle `requestFloor` differently) — behavior lives in the state class, and you delete the giant `switch` repeated across methods.

Say the trade-off out loud: State pattern = one class per state (more files, open for extension); table = one map (compact, but every event method still branches).


## Q zh
转变表/枚举 vs GoF 状态模式（每个状态一个类）— 你在一个计时的机器编码轮次怎样选择?

## A zh
决定通过**复杂性在哪里**:

- **表/枚举**当逻辑**是**转变和每个状态行为是平凡的时（订单生命周期、预订状态）。远更少代码 — 在时间压力下的正确默认。
- **状态模式**当每个状态携带**实质上不同的行为**（电梯: MovingUp/DoorOpen/Idle 各自处理 `requestFloor` 不同）— 行为生活在状态类中，你删除重复的大 `switch` 跨方法。

大声说权衡: 状态模式 = 每个状态一个类（更多文件、对扩展开放）；表 = 一个地图（紧凑，但每个事件方法仍然分支）。
