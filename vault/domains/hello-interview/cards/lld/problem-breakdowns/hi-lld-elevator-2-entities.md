---
id: hi-lld-elevator-2-entities
node: lld.problem-breakdowns.elevator.exam
type: qa
step: 2
---
## Q
**核心实体：谁是类，谁只是整数**｜低层设计 · 题目拆解

电梯系统里 Floor、Request、Elevator、ElevatorController 这几个名词，哪些该做成类，哪些不该？为什么？

## A
**要点。**

| 候选 | 结论 | 理由 |
|---|---|---|
| Floor | 不做类，用 `int` | 没有状态也没有规则，只是位置编号 |
| Elevator | 类 | 有当前楼层、方向、待停楼层，还要守规则（沿路径停靠、不低于 0 层） |
| ElevatorController | 类 | 收呼叫、选电梯、拥有 `step()` 推进全局时间 |
| Request | 先搁置，类设计时再定 | 看它是不是只包了一个整数 |

**为什么。** 凡是时间驱动的模拟，都需要一个控制器持有 `step()`，协调所有参与者。

**取舍。** 暂时拿不准的实体，可以直接告诉面试官「先悬着，学到更多运动逻辑后再定」，这是正常的，不是失误。
