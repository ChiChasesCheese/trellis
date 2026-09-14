---
id: cc-performance-amortized-incremental-aggregate
node: performance.amortized
type: qa
---
## Q
Every event must report the current total across all merchants. `sum(balances.values())` per event is O(m). What replaces it, and what is the risk you take on?

## A
**Maintain the aggregate incrementally: adjust `total` by the delta in the same statement that changes a balance.** O(1) per event instead of O(m).

The risk is **two sources of truth**. Every mutation path must apply the same delta — including the rare ones: reversals, refunds, a de-duplicated replay that must *not* apply a delta, and a bulk load.

- Discipline: funnel all mutations through one function that updates both, so there is exactly one place to be wrong.
- Cross-check `total == sum(balances.values())` in a test, never in the hot loop ([[cc-verification-invariant-assert-cost]]).

## Q zh
每个事件都要报出所有商户的当前总额。每次事件做 `sum(balances.values())` 是 O(m)。用什么替代？你因此承担了什么风险？

## A zh
**增量维护聚合值：在改动某个余额的同一条语句里，把 `total` 按差量调整。** 每事件 O(1)，而不是 O(m)。

风险是**两个真相来源**。每一条变更路径都必须施加同样的差量 —— 包括那些罕见的：冲正、退款、一次去重后**不该**施加差量的重放、以及批量导入。

- 纪律：把所有变更收敛到同一个函数里，让它同时更新两者，这样只有一个地方可能出错。
- 在测试里交叉验证 `total == sum(balances.values())`，绝不放进热点循环（[[cc-verification-invariant-assert-cost]]）。
