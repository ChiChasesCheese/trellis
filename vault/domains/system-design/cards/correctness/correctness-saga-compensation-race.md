---
id: correctness-saga-compensation-race
node: correctness.saga
type: qa
---
## Q
A saga cancellation can race its own forward action: the "release seat" compensation arrives at a participant **before** the delayed "reserve seat" command. What happens, and what's the fix?

## A
Naively, the release is a no-op ("nothing reserved"), then the late reserve lands and **holds the seat forever** — the saga believes it rolled back, the participant disagrees.

Fix: compensation must be a **tombstone, not just an undo**. The participant records "saga X: cancelled" so a forward command arriving after its own compensation is **rejected**, not applied. Requires per-saga state at the participant and a retention window longer than max command delay.

General rule: with at-least-once delivery and no ordering across queues, every participant must handle each saga command **in any order and any multiplicity** — commutativity of cancel-before-act is part of the contract.

## Q zh
saga 取消可与自己的前向操作竞态：「释放座位」补偿到达参与者**之前**延迟的「预订座位」命令。发生什么，修复什么？

## A zh
天真地，释放是空操作（「什么都没预留」），然后晚到预留着陆并**永远持有座位** — saga 相信它回滚，参与者不同意。

修复：补偿必须是**墓碑，不仅是撤销**。参与者记录「saga X：已取消」，这样在自己补偿之后到达的前向命令**被拒绝**，不应用。需要参与者的每 saga 状态和长于最大命令延迟的保留窗口。

通用规则：带至少一次交付和跨队列无排序，每个参与者必须以**任何顺序和任何复数**处理每个 saga 命令 — 取消-前操作的交换律是契约的一部分。
