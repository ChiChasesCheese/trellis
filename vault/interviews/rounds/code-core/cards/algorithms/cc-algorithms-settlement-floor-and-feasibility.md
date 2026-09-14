---
id: cc-algorithms-settlement-floor-and-feasibility
node: algorithms.settlement
type: qa
---
## Q
Every account must end holding at least `MIN`. When is it impossible, and what constrains each individual transfer?

## A
**Feasible iff `sum(balances) >= MIN * n`** — non-strict, because everyone landing exactly on `MIN` is a valid end state; one unit less is `IMPOSSIBLE`.

- Per account, surplus is `balance − MIN` and deficit is `MIN − balance`. The sum of surpluses covers the sum of deficits exactly when the global test passes, which is why the test is sufficient and not merely necessary.
- **A transfer must never push its source below `MIN`** — the floor applies during the run, not only at the end — and must be strictly positive; a zero-amount transfer is noise, not an answer.
- "Already all at or above `MIN`" produces **no transfers**, which is a different output from `IMPOSSIBLE` and from an error ([[cc-output-sentinels-none-vs-blank]]).
- Negative balances are legal inputs; they are simply large deficits. So is a single account, and two accounts.
- Check feasibility before constructing, so a failing greedy is a bug in the greedy ([[cc-algorithms-greedy-feasibility-first]]).

## Q zh
每个账户最终必须至少持有 `MIN`。什么时候不可能，每一笔转账又受什么约束？

## A zh
**可行当且仅当 `sum(balances) >= MIN * n`** —— 非严格，因为所有人恰好落在 `MIN` 上是合法终态；少一个单位就是 `IMPOSSIBLE`。

- 每个账户的盈余是 `balance − MIN`，缺口是 `MIN − balance`。当全局判据通过时，盈余之和恰好覆盖缺口之和，这也是该判据不仅必要而且充分的原因。
- **转账绝不能把源账户压到 `MIN` 以下** —— 下限在过程中就生效，而不只是在结束时 —— 而且金额必须严格为正；零额转账是噪音，不是答案。
- 「本来就都不低于 `MIN`」产生**零笔转账**，这与 `IMPOSSIBLE` 不同，也与报错不同（[[cc-output-sentinels-none-vs-blank]]）。
- 负余额是合法输入；它们只是很大的缺口。只有一个账户、只有两个账户也一样。
- 在构造之前先检查可行性，这样贪心失败就是贪心自身的 bug（[[cc-algorithms-greedy-feasibility-first]]）。
