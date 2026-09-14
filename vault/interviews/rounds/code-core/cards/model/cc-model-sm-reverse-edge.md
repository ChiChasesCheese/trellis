---
id: cc-model-sm-reverse-edge
node: model.state-machine
type: qa
---
## Q
`FAIL` moves a payment from `PROCESSING` back to `REQUIRES_ACTION`. What does that one backward edge change about the rest of the machine?

## A
**It makes the earlier state reachable again, so every rule phrased as "only before X" comes back into force.**

`UPDATE` was ignored after `ATTEMPT`; after a `FAIL` it applies again, and a later `SUCCEED` must credit the **updated** amount. Any code that recorded "has been attempted" as a one-way latch is now wrong.

The lesson generalizes: a state machine with a cycle has no "already past that" shortcuts. Test the loop explicitly — attempt, fail, update, attempt, succeed — because a linear implementation passes every straight-line test and fails only that one.

## Q zh
`FAIL` 把付款从 `PROCESSING` 退回 `REQUIRES_ACTION`。这一条回边改变了机器的其余部分的什么？

## A zh
**它让更早的状态重新可达，于是所有"只在 X 之前"的规则重新生效。**

`UPDATE` 在 `ATTEMPT` 之后被忽略；而在 `FAIL` 之后它又生效，随后的 `SUCCEED` 必须入账**更新后**的金额。任何把"已经 attempt 过"记成单向闩锁的代码，现在都是错的。

教训可推广：带环的状态机没有"已经过了那个阶段"的捷径。显式测试这个环 —— attempt、fail、update、attempt、succeed —— 因为线性实现能通过所有直线测试，唯独在这一条上失败。
