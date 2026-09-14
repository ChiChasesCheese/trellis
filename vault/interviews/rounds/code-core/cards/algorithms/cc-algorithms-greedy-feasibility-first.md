---
id: cc-algorithms-greedy-feasibility-first
node: algorithms.greedy
type: qa
---
## Q
Every account must end at or above a minimum. When do you declare it impossible — before or after running the greedy?

## A
**Before, with a counting argument:** feasible iff `sum(balances) >= minimum * n`, non-strict, since everyone landing exactly on the minimum is a valid end state.

- Separating feasibility from construction means a greedy that fails is a bug in *your greedy*, not evidence of impossibility. Without the separation you cannot tell the two apart, and you will "fix" the wrong one.
- The check is O(n) and answers the `IMPOSSIBLE` output directly ([[cc-algorithms-settlement-floor-and-feasibility]]).
- The mirror rule during construction: a transfer must never push its **source** below the floor, so the usable surplus is `balance − minimum`, not `balance`.
- "Already all above the minimum" is a third case — no transfers, which is neither `IMPOSSIBLE` nor an error ([[cc-output-sentinels-none-vs-blank]]).

## Q zh
每个账户最终都必须不低于某个最小值。你在什么时候判定不可能 —— 跑贪心之前还是之后？

## A zh
**之前，用一个计数论证：** 可行当且仅当 `sum(balances) >= minimum * n`，非严格，因为所有人恰好落在最小值上是合法的终态。

- 把可行性与构造分开，意味着贪心失败时那是*你的贪心*有 bug，而不是不可能的证据。不分开你就分不清两者，然后会去「修」错的那个。
- 这个检查是 O(n)，并直接给出 `IMPOSSIBLE` 的输出（[[cc-algorithms-settlement-floor-and-feasibility]]）。
- 构造阶段的镜像规则：转账绝不能把**源账户**压到下限之下，所以可用盈余是 `balance − minimum` 而不是 `balance`。
- 「本来就都高于最小值」是第三种情形 —— 不需要任何转账，它既不是 `IMPOSSIBLE` 也不是错误（[[cc-output-sentinels-none-vs-blank]]）。
