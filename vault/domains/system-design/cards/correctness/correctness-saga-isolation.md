---
id: correctness-saga-isolation
node: correctness.saga
type: qa
---
## Q
Sagas have ACD but no I. What anomalies does the missing isolation cause, and name the standard countermeasures.

## A
Each step commits locally, so **intermediate state is visible** before the saga's fate is known:

- **Dirty read**: another flow sees "payment captured" and ships — then the saga compensates. The world acted on state that got undone.
- **Lost update**: a concurrent writer modifies the row between a step and its compensation; the compensation stomps it.

Countermeasures (Garcia-Molina lineage):
- **Semantic lock**: write a `PENDING` marker; other transactions must skip/wait/reject pending resources.
- **Commutative updates** (± deltas) so interleavings don't matter.
- **Version check / reread** before compensating — compensate only what you actually did.
- **Reordering**: put the riskiest, non-compensatable step last (the pivot, [[correctness-saga-compensation-limits]]).

## Q zh
Saga 有 ACD 但没 I。缺失隔离导致什么异常，命名标准对策。

## A zh
每步本地提交，所以**中间状态可见**在 saga 的命运已知前：

- **脏读**：另一流程看「支付已交割」和发货 — 然后 saga 补偿。世界作用在被撤销的状态上。
- **丢失更新**：并发写在步骤和其补偿间修改行；补偿踩掉它。

对策（Garcia-Molina 血统）：
- **语义锁**：写 `PENDING` 标记；其他交易必须跳过/等待/拒绝 pending 资源。
- **交换律更新**（± 增量）交错不重要。
- **版本检查 / 重读**补偿前 — 仅补偿你实际做的。
- **重排序**：最后放风险最大、不可补偿的步骤（转折点，[[correctness-saga-compensation-limits]]）。
